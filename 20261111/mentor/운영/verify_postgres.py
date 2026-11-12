"""새 검수 DB에서 강사용 SQL을 실제 실행하는 선택 도구입니다.
기본 --emit-only는 파일 생성뿐입니다. 실제 서버 작업은 --run이 필요합니다.
Python 표준 라이브러리와 psql만 사용하며, 수업용 knowledge_lab은 초기화하지 않습니다.
"""
from __future__ import annotations
import argparse, getpass, json, os, re, shutil, subprocess, sys, time, uuid
from pathlib import Path
from sql_tools import parse_steps, capture_once, replace_runtime_ids, mask_sql

ROOT=Path(__file__).resolve().parents[1]
LEVELS={'B':'01_기본필수','A':'02_응용','H':'03_심화'}

def rows(table='knowledge',where=''):
    return f"(SELECT COALESCE(jsonb_agg(to_jsonb(t) ORDER BY id),'[]'::jsonb) FROM public.{table} t {where})"

def save(name,table='knowledge',where=''):
    return f'SELECT {rows(table,where)} AS data\n\\gset {name}_\n'

def check(label,condition):
    return (f'SELECT COALESCE(({condition}),false) AS ok\n\\gset check_\n'
            f'\\if :check_ok\n\\echo @@PASS {label}\n\\else\n\\echo @@FAIL {label}\n'
            'SELECT 1 / 0;\n\\endif\n')

READ_ORACLES = {
    'E2_LIST': "VALUES (1,'실습 파일 보관',1),(2,'서버 실행',2),(3,'질문 작성',1)",
    'E2_DETAIL': "VALUES (2,'서버 실행','프로젝트 폴더에서 서버를 실행합니다.')",
    'E2_CATEGORY': "VALUES (1,'실습 파일 보관'),(3,'질문 작성')",
    'E2_EMPTY': "SELECT id,title FROM public.knowledge WHERE false",
    'E2_COMBINED': "VALUES (1,'실습 파일 보관')",
    'E2_NULL': "VALUES (NULL::text,TRUE)",
    'E2_TIE': "VALUES (1,10),(3,10),(2,5)",
    'E3_READ': "VALUES (1,'안내',1)",
    'E5_JOIN': "VALUES (1,'실습 파일 보관','learning'),(2,'서버 실행','environment'),(3,'질문 작성','learning')",
    'E5_GROUP': "VALUES ('learning',2),('environment',1),('reference',0)",
    'E5_LENGTH': "VALUES (3,64,20,24)",
    'E5_HAVING': "VALUES ('learning',2)",
    'E5_ON': "VALUES ('learning',1),('environment',0),('reference',0)",
    'E5_WHERE': "VALUES ('learning',1)",
}

def read_result_check(step, sql):
    # 실제 과제 SELECT 결과를 다중집합으로 비교합니다. 중복 행도 검출합니다.
    actual=mask_sql(sql,strings=False).strip().removesuffix(';').strip()
    expected=READ_ORACLES[step]
    condition=(f"NOT EXISTS (({actual}) EXCEPT ALL ({expected})) "
               f"AND NOT EXISTS (({expected}) EXCEPT ALL ({actual}))")
    return check(step+'_RESULT',condition)

def compile_level(level,dbname,root=ROOT):
    folder=root/LEVELS[level]
    order=json.loads((folder/'exercise_order.json').read_text(encoding='utf-8'))
    src=['\\set ON_ERROR_STOP on','\\set ON_ERROR_ROLLBACK off','\\set AUTOCOMMIT on',
         '\\set VERBOSITY verbose','\\pset tuples_only on','\\pset format unaligned',
         "SET client_encoding TO 'UTF8';",(root/'00_준비/01_prepare_S0.sql').read_text(encoding='utf-8')]
    src.append(check('S0_COUNTS',"(SELECT COUNT(*) FROM public.categories)=3 AND (SELECT COUNT(*) FROM public.knowledge)=3"))
    src.append(check('S0_LENGTHS',"(SELECT SUM(char_length(content)) FROM public.knowledge)=64"))
    src.append(check('S0_GROUP',"(SELECT COUNT(*) FROM public.knowledge k JOIN public.categories c ON c.id=k.category_id WHERE c.name='learning')=2"))
    expected={}
    for ex in range(1,9):
        if ex==8:
            # N=3을 고정하는 오류를 잡기 위한 검수 DB 전용 기존 지식입니다.
            src.append("INSERT INTO public.knowledge(title,content,category_id) SELECT '검수 전 기존 지식','이 기존 지식도 마지막까지 보존합니다.',id FROM public.categories WHERE name='reference';")
        src.extend([save(f'pre{ex}'),save(f'pre{ex}_categories','categories')])
        for path in order[str(ex)]:
            for s in parse_steps((folder/path).read_text(encoding='utf-8')):
                if s.key in expected:raise ValueError('중복 구간 '+s.key)
                expected[s.key]=s.expect
                if s.reconnect:
                    src.extend(['SELECT pg_backend_pid() AS pid\n\\gset before_connection_',
                                '\\connect '+dbname,
                                check(s.key+'_NEW_CONNECTION','pg_backend_pid() <> :before_connection_pid')])
                sql=replace_runtime_ids(s.sql)
                if s.expect!='00000':src.append('\\set ON_ERROR_STOP off')
                src.append(capture_once(sql,s.capture) if s.capture!='-' else sql)
                src.append(f'\\echo @@STATE {s.key} :SQLSTATE')
                if s.expect!='00000':src.append('\\set ON_ERROR_STOP on')
                if s.key in READ_ORACLES:src.append(read_result_check(s.key,sql))
                if s.key=='E1_DB':src.append(check('CONNECTED_DB',f"current_database()='{dbname}'"))
                if s.key=='E3_GONE':src.append(check('TRY_GONE',"to_regclass('public.categories_try') IS NULL AND to_regclass('public.knowledge_try') IS NULL"))
                if s.key=='E7_CANCEL_READ':src.append(check('E7_CANCEL_DATA',rows()+"=:'pre7_data'::jsonb"))
                if s.key=='E7_RECONNECT':
                    src.append(check('E7_SAVED',"(SELECT content FROM public.knowledge WHERE id=2)='실행 전에 가상환경을 확인합니다.'"));src.append(save('s1'))
                if s.key in ('E7_PAIR_CANCEL','E7_ATOMIC_AFTER'):
                    src.append(check(s.key+'_UNCHANGED',rows()+"=:'s1_data'::jsonb"))
                if s.key=='D8_BASELINE':
                    src.extend(['SELECT COUNT(*) AS n FROM public.knowledge\n\\gset project_',save('project_start')])
                if s.key=='D8_CREATE_A':src.append(save('project_a',where='WHERE id=:a_id'))
                if s.key=='D8_CREATE_B':src.append(save('project_b',where='WHERE id=:b_id'))
                if s.key=='D8_CREATE_COMMIT':
                    src.append(check('D8_N_PLUS_3','(SELECT COUNT(*) FROM public.knowledge)=:project_n+3'))
                    src.append(check('D8_DISTINCT_IDS',':a_id<>:b_id AND :b_id<>:c_id AND :a_id<>:c_id'))
                if s.key=='D8_B_RESTORED':src.append(check('D8_B_CANCELLED',rows(where='WHERE id=:b_id')+"=:'project_b_data'::jsonb"))
                if s.key=='D8_B_RECONNECT':
                    src.append(check('D8_B_SAVED',"(SELECT content FROM public.knowledge WHERE id=:b_id)='결과에는 실행 명령과 실제 SQL 결과를 함께 적습니다.'"))
                    src.append(check('D8_B_OTHER_FIELDS',"(SELECT to_jsonb(t)-'content' FROM public.knowledge t WHERE id=:b_id)=((:'project_b_data'::jsonb->0)-'content')"))
                if s.key=='D8_ERRORS_BEFORE':src.append(save('before_errors'))
                if s.key=='D8_ERRORS_AFTER':src.append(check('D8_ERROR_PRESERVES',rows()+"=:'before_errors_data'::jsonb"))
        if ex<7:
            src.append(check(f'E{ex}_ROWS_UNCHANGED',rows()+f"=:'pre{ex}_data'::jsonb"))
            src.append(check(f'E{ex}_CATS_UNCHANGED',rows('categories')+f"=:'pre{ex}_categories_data'::jsonb"))
        if ex==7:
            src.append(check('E7_OTHER_ROWS_UNCHANGED',"(SELECT COALESCE(jsonb_agg(x ORDER BY x->>'id'),'[]'::jsonb) FROM jsonb_array_elements("+rows()+") x WHERE x->>'id'<>'2') = (SELECT COALESCE(jsonb_agg(x ORDER BY x->>'id'),'[]'::jsonb) FROM jsonb_array_elements(:'pre7_data'::jsonb) x WHERE x->>'id'<>'2')"))
            src.append(check('INDEX_PRESENT',"EXISTS(SELECT 1 FROM pg_indexes WHERE schemaname='public' AND tablename='knowledge' AND indexname='idx_knowledge_category_id')"))
        if ex==8:
            src.append(check('D8_FINAL_N_PLUS_2','(SELECT COUNT(*) FROM public.knowledge)=:project_n+2'))
            src.append(check('D8_C_ABSENT','NOT EXISTS(SELECT 1 FROM public.knowledge WHERE id=:c_id)'))
            src.append(check('D8_A_PRESERVED',rows(where='WHERE id=:a_id')+"=:'project_a_data'::jsonb"))
            src.append(check('D8_OLD_PRESERVED',rows(where='WHERE id NOT IN (:a_id,:b_id)')+"=:'project_start_data'::jsonb"))
            src.append(check('D8_CATS_PRESERVED',rows('categories')+"=:'pre8_categories_data'::jsonb"))
            src.append(check('D8_GROUP_TOTAL',"(SELECT SUM(n) FROM (SELECT COUNT(k.id) n FROM public.categories c LEFT JOIN public.knowledge k ON k.category_id=c.id GROUP BY c.id) g)=(SELECT COUNT(*) FROM public.knowledge)"))
    src.append('\\echo @@COMPLETE '+level)
    return '\n\n'.join(src)+'\n',expected

def psql_call(executable,args,env,sql=None,file=None,db=None):
    cmd=[executable,'-X','-h',args.host,'-p',str(args.port),'-U',args.user,'-d',db or args.maintenance_db,
         '-v','ON_ERROR_STOP=1','-P','pager=off','-w']
    cmd+=['-f',str(file)] if file is not None else ['-c',sql or 'SELECT 1;']
    return subprocess.run(cmd,env=env,text=True,encoding='utf-8',errors='replace',capture_output=True,timeout=args.timeout)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    mode=p.add_mutually_exclusive_group();mode.add_argument('--run',action='store_true');mode.add_argument('--emit-only',action='store_true')
    p.add_argument('--host',default='localhost');p.add_argument('--port',type=int,default=5432);p.add_argument('--user',default='postgres')
    p.add_argument('--maintenance-db',default='postgres');p.add_argument('--psql',default='psql')
    p.add_argument('--password-prompt',action='store_true');p.add_argument('--cleanup',action='store_true',help='이번 실행이 만든 검수 DB만 삭제')
    p.add_argument('--levels',nargs='+',choices=list(LEVELS),default=list(LEVELS))
    p.add_argument('--output',type=Path,default=Path('day18_verification'));p.add_argument('--root',type=Path,default=ROOT)
    p.add_argument('--timeout',type=int,default=120)
    a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    report={'mode':'actual_postgresql' if a.run else 'emit_only','date':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'cases':[]}
    def write_report():
        (a.output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    exe=shutil.which(a.psql) or (str(Path(a.psql).resolve()) if Path(a.psql).is_file() else None)
    if a.run and not exe:
        report.update(status='not_run',reason='psql 실행 파일이 없습니다.');write_report();print(report['reason'],file=sys.stderr);return 2
    env=os.environ.copy();env.update(PGCLIENTENCODING='UTF8',PGCONNECT_TIMEOUT='10')
    if a.run and a.password_prompt:env['PGPASSWORD']=getpass.getpass('DB 비밀번호(저장하지 않음): ')
    if a.run:
        try:v=psql_call(exe,a,env,sql="SELECT version(),current_setting('server_version_num');")
        except (OSError,subprocess.TimeoutExpired) as e:
            report.update(status='not_run',reason=str(e));write_report();return 2
        report['server_version_output']=v.stdout.strip()
        if v.returncode:
            report.update(status='connection_failed',error=v.stderr.strip());write_report();return 2
    failed=False
    for level in a.levels:
        db='knowledge_lab_verify_'+uuid.uuid4().hex[:12]
        try:script,expected=compile_level(level,db,a.root)
        except (OSError,ValueError) as e:
            report['cases'].append({'level':level,'status':'compile_failed','error':str(e)});failed=True;continue
        f=a.output/f'{level}_verification.psql';f.write_text(script,encoding='utf-8')
        case={'level':level,'database':db,'expected_steps':len(expected),'status':'not_executed'}
        if not a.run:report['cases'].append(case);continue
        made=False
        try:
            if not re.fullmatch(r'knowledge_lab_verify_[0-9a-f]{12}',db):raise ValueError('검수 DB 이름 오류')
            cr=psql_call(exe,a,env,sql=f'CREATE DATABASE "{db}";')
            if cr.returncode:raise RuntimeError('검수 DB 생성 실패: '+cr.stderr.strip())
            made=True
            r=psql_call(exe,a,env,file=f,db=db)
            (a.output/f'{level}_stdout.txt').write_text(r.stdout,encoding='utf-8')
            (a.output/f'{level}_stderr.txt').write_text(r.stderr,encoding='utf-8')
            states=dict(re.findall(r'^@@STATE\s+(\w+)\s+(\w+)\s*$',r.stdout,re.M))
            bad={k:{'expected':v,'actual':states.get(k)} for k,v in expected.items() if states.get(k)!=v}
            ok=r.returncode==0 and not bad and '@@COMPLETE '+level in r.stdout and '@@FAIL' not in r.stdout
            case.update(status='passed' if ok else 'failed',returncode=r.returncode,observed_steps=len(states),state_mismatches=bad,
                        passed_assertions=len(re.findall(r'^@@PASS ',r.stdout,re.M)))
            failed|=not ok
        except (OSError,ValueError,RuntimeError,subprocess.TimeoutExpired) as e:case.update(status='failed',error=str(e));failed=True
        finally:
            if made and a.cleanup:
                try:
                    dr=psql_call(exe,a,env,sql=f'DROP DATABASE "{db}";')
                    case['cleanup']='removed' if dr.returncode==0 else 'failed'
                    if dr.returncode:case['cleanup_error']=dr.stderr.strip();failed=True
                except (OSError,subprocess.TimeoutExpired) as e:case['cleanup_error']=str(e);failed=True
            elif made:case['cleanup']='kept_for_inspection'
        report['cases'].append(case)
    report['status']='failed' if failed else ('passed' if a.run else 'not_executed')
    write_report();print(json.dumps(report,ensure_ascii=False,indent=2));return 1 if failed else 0

if __name__=='__main__':raise SystemExit(main())
