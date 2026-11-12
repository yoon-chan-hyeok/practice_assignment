"""강사용 선택 검수. 새 day19_check_* DB만 생성하며 기존 DB를 삭제하지 않습니다.
설치: python -m pip install 'psycopg[binary]'
실행: python verify_postgres.py --allow-test-db-creation --host localhost --user postgres
비밀번호는 libpq의 안전한 passfile을 사용하거나 --ask-password로 입력합니다.
"""
from __future__ import annotations
import argparse
import getpass
import json
import os
from pathlib import Path
import re
import sys
import uuid


def extract_case(path: Path, case: str) -> str:
    match = re.search(rf"(?ms)^-- CASE {re.escape(case)}\n(.*?)^-- ENDCASE {re.escape(case)}\s*$", path.read_text(encoding="utf-8"))
    if not match:
        raise ValueError(f"CASE {case} not found: {path.name}")
    return match.group(1)


def collect(conn, sql_text: str) -> list[dict]:
    output = []
    with conn.cursor() as cur:
        cur.execute(sql_text, prepare=False)
        while True:
            if cur.description:
                output.append({"columns": [d.name for d in cur.description], "rows": [list(row) for row in cur.fetchall()]})
            if not cur.nextset():
                break
    return output


def snapshot(conn) -> list:
    return collect(conn, "SELECT id,title,content,category_id FROM public.knowledge ORDER BY id;")[0]["rows"]


def verify_structure(conn, tag: str, checked: list[str]) -> None:
    rows = collect(conn, """SELECT table_name,column_name,data_type,character_maximum_length,is_nullable,is_identity,identity_generation
        FROM information_schema.columns WHERE table_schema='public' AND table_name IN ('categories','knowledge')
        ORDER BY table_name,ordinal_position;""")[0]["rows"]
    expected = [
        ['categories','id','bigint',None,'NO','YES','ALWAYS'],
        ['categories','name','character varying',30,'NO','NO',None],
        ['knowledge','id','bigint',None,'NO','YES','ALWAYS'],
        ['knowledge','title','character varying',80,'NO','NO',None],
        ['knowledge','content','text',None,'NO','NO',None],
        ['knowledge','category_id','bigint',None,'NO','NO',None],
    ]
    assert rows == expected, f"{tag}: 열 정의 불일치"
    constraints = collect(conn, """SELECT conname,contype::text,confdeltype::text
       FROM pg_constraint WHERE conrelid IN ('public.categories'::regclass,'public.knowledge'::regclass);""")[0]['rows']
    types = [r[1] for r in constraints]
    assert types.count('p') == 2 and types.count('u') == 1 and types.count('f') == 1
    assert ['knowledge_category_fk','f','r'] in constraints
    for name in ('categories_name_length','knowledge_title_length','knowledge_content_length'):
        assert any(row[0] == name and row[1] == 'c' for row in constraints), name
    if tag == 'H':
        definition = collect(conn, "SELECT indexdef FROM pg_indexes WHERE schemaname='public' AND indexname='idx_knowledge_category_id';")[0]['rows']
        assert len(definition)==1 and 'USING btree (category_id)' in definition[0][0]
    checked.append(f'{tag}: 열·IDENTITY·PK/UQ/FK/CHECK·삭제정책'+('·인덱스' if tag=='H' else ''))


def run(args) -> dict:
    try:
        import psycopg
        from psycopg import sql
    except ImportError as exc:
        raise RuntimeError("검수용 psycopg가 필요합니다. 학생용 실습에는 필요하지 않습니다.") from exc
    if not args.allow_test_db_creation:
        raise ValueError("새 검수 DB 생성을 허용하려면 --allow-test-db-creation을 지정하세요.")
    prefix = args.prefix or ('day19_check_'+uuid.uuid4().hex[:8])
    if not re.fullmatch(r'day19_check_[a-z0-9]{4,18}',prefix):
        raise ValueError("검수 DB 접두어는 day19_check_와 영문 소문자/숫자 4~18자리여야 합니다.")
    folder = Path(__file__).resolve().parent
    role_root = folder.parent
    manifest = json.loads((folder/'SQL_CASES.json').read_text(encoding='utf-8'))
    password = getpass.getpass('DB 비밀번호(화면에 표시 안 됨): ') if args.ask_password else None
    settings = dict(host=args.host,port=args.port,user=args.user,connect_timeout=8,autocommit=True)
    if password is not None:
        settings['password'] = password
    checked=[]; databases=[]
    try:
        with psycopg.connect(dbname=args.admin_db,**settings) as admin:
            server_version=admin.info.server_version
            if server_version < 180000:
                print('안내: 자료 기준은 PostgreSQL 18입니다. 실제 서버 버전은 결과에 기록합니다.')
            for tag,meta in manifest.items():
                pg=role_root/meta['level']/'02_PostgreSQL'
                for kind in ('build','crud'):
                    name=f'{prefix}_{kind}_{tag.lower()}'
                    if admin.execute('SELECT 1 FROM pg_database WHERE datname=%s',(name,)).fetchone():
                        raise RuntimeError(f'이미 존재하는 검수 DB에는 실행하지 않습니다: {name}')
                    admin.execute(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(name)))
                    databases.append(name)
                    with psycopg.connect(dbname=name,**settings) as conn:
                        original=meta[f'{kind}_db']
                        files=meta['build_files'] if kind=='build' else ['B_CRUD/00_ready_database.sql']
                        for relative in files:
                            text=(pg/relative).read_text(encoding='utf-8').replace(original,name)
                            if re.search(r'__TODO_[A-Z0-9_]+__',text):
                                raise ValueError(f'미완성 TODO: {relative}')
                            collect(conn,text)
                        verify_structure(conn,tag,checked)
                        if kind=='build':
                            collect(conn,(pg/'A_구축/check_insert.sql').read_text(encoding='utf-8').replace(original,name))
                            assert snapshot(conn)==[]
                            checked.append(f'{tag}: 구축 점검 INSERT·JOIN·ROLLBACK')
                            continue
                        baseline=snapshot(conn)
                        assert len(baseline)==3
                        new_id=None
                        for case in meta['cases']:
                            text=extract_case(pg/case['file'],case['id'])
                            if '__NEW_ID__' in text:
                                if new_id is None: raise ValueError('C01이 먼저 필요합니다.')
                                text=text.replace('__NEW_ID__',str(new_id))
                            actual=collect(conn,text)
                            if case['id'].startswith('R'):
                                assert actual[-1] == case['expected'], (case['id'],actual,case['expected'])
                                assert snapshot(conn)==baseline
                            elif case['id']=='C01':
                                assert len(actual[0]['rows'])==1
                                new_id=actual[0]['rows'][0][0]
                                assert new_id not in [r[0] for r in baseline]
                                assert actual[-1]['rows']==[[4]]
                                assert collect(conn,f'SELECT title,content,category_id FROM public.knowledge WHERE id={new_id};')[0]['rows']==[['보충 학습','복습 자료는 개인 폴더에서 확인합니다.',1]]
                            elif case['id']=='U01':
                                assert actual[0]['rows']==[[new_id,'복습 자료와 예제 코드를 함께 확인합니다.']]
                                assert actual[-1]['rows']==[[new_id,'복습 자료는 개인 폴더에서 확인합니다.']]
                            elif case['id']=='U02':
                                assert actual[0]['rows']==actual[-1]['rows']==[[new_id,'복습 자료와 예제 코드를 함께 확인합니다.']]
                            elif case['id']=='D01':
                                assert actual[0]['rows']==[[new_id]] and actual[1]['rows']==[]
                                assert snapshot(conn)==baseline
                            elif case['id']=='T01':
                                assert snapshot(conn)==baseline
                            checked.append(f'{tag}: {case["id"]} 실제 SQL·예상값')
                        for err in meta['errors']:
                            before=snapshot(conn)
                            try:
                                collect(conn,extract_case(pg/'B_CRUD/errors.sql',err['id']))
                            except psycopg.Error as exc:
                                assert exc.sqlstate==err['sqlstate'],(err['id'],exc.sqlstate)
                                if err['constraint']: assert exc.diag.constraint_name==err['constraint']
                                conn.execute('ROLLBACK;')
                            else:
                                conn.execute('ROLLBACK;')
                                raise AssertionError(f'{err["id"]}: 기대 오류가 발생하지 않음')
                            assert snapshot(conn)==before
                            checked.append(f'{tag}: {err["id"]} {err["sqlstate"]}·오류 후 보존')
                        assert snapshot(conn)==baseline
        return {'status':'passed','postgresql_version_number':server_version,'check_count':len(checked),'checks':checked,'created_test_databases':databases,'cleanup':'자동 DROP 없음. 필요한 검수 DB만 관리자가 나중에 정리하세요.'}
    except Exception:
        print('이번 검수에서 생성된 DB:', ', '.join(databases) or '(없음)',file=sys.stderr)
        raise


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allow-test-db-creation',action='store_true')
    parser.add_argument('--host',default=os.environ.get('PGHOST','localhost'))
    parser.add_argument('--port',type=int,default=int(os.environ.get('PGPORT','5432')))
    parser.add_argument('--user',default=os.environ.get('PGUSER','postgres'))
    parser.add_argument('--admin-db',default='postgres')
    parser.add_argument('--ask-password',action='store_true')
    parser.add_argument('--prefix')
    parser.add_argument('--output',type=Path,default=Path('postgres_verification_result.json'))
    args=parser.parse_args()
    try:
        result=run(args)
    except Exception as exc:
        # Never print connection URLs or passwords.
        print(f'검수 실패: {type(exc).__name__}: {exc}',file=sys.stderr)
        return 1
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'실제 PostgreSQL 확인 {result["check_count"]}개 통과. 기록: {args.output}')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
