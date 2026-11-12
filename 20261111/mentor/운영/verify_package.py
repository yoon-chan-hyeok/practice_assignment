"""SQL을 DB에 보내지 않는 정적 검수. SQL 실행 검증과 구분합니다."""
from __future__ import annotations
import argparse, ast, json, re, sys
from pathlib import Path
from sql_tools import mask_sql, parse_steps, capture_once, replace_runtime_ids

ROLE=Path(__file__).resolve().parents[1]
LEVELS=['01_기본필수','02_응용','03_심화']
BLOCK=re.compile(r'^-- BEGIN TASK (\w+)\n.*?^-- END TASK \1\s*$',re.M|re.S)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--instructor',type=Path,default=ROLE)
    parser.add_argument('--student',type=Path,default=ROLE.parent/'수강생용')
    parser.add_argument('--output',type=Path,default=Path('static_report.json'))
    args=parser.parse_args();teacher=args.instructor;student=args.student
    report={'scope':'static_only','sql_execution':False,'checks':[]}
    def check(label,ok,detail=''):
        report['checks'].append({'label':label,'passed':bool(ok),'detail':detail})
    all_tasks=set();pairs=0;step_count=0
    for level,prefix,count in zip(LEVELS,['B','A','H'],[18,26,33]):
        folder=teacher/level;order=json.loads((folder/'exercise_order.json').read_text(encoding='utf-8'))
        check(level+'_eight_exercises',set(order)==set(map(str,range(1,9))))
        level_ids=[];keys=set()
        for ex,paths in order.items():
            for path in paths:
                text=(folder/path).read_text(encoding='utf-8');code=mask_sql(text)
                tblocks={m[1]:m[0] for m in BLOCK.finditer(text)};level_ids.extend(tblocks)
                check(path+'_no_unfinished_teacher_sql','__TODO_' not in code)
                check(path+'_no_drop_or_truncate',not re.search(r'\b(DROP|TRUNCATE)\b',code,re.I))
                check(path+'_no_psql_in_gui_sql',not re.search(r'^\s*\\',code,re.M))
                # Lexical boundary check, not a PostgreSQL grammar parser.
                check(path+'_balanced_parentheses',code.count('(')==code.count(')'))
                steps=parse_steps(text)
                for s in steps:
                    check(s.key+'_unique',s.key not in keys);keys.add(s.key)
                    check(s.key+'_state_format',bool(re.fullmatch(r'[0-9A-Z]{5}',s.expect)))
                    if s.capture!='-':
                        captured=capture_once(replace_runtime_ids(s.sql),s.capture)
                        check(s.key+'_single_capture',captured.count('\\gset '+s.capture)==1)
                    if s.expect!='00000':check(s.key+'_known_expected_error',s.expect in ['23514','23503','23502','23505','25P02'])
                    step_count+=1
                sfile=student/level/path
                if student.exists():
                    check(path+'_student_exists',sfile.is_file())
                    stext=sfile.read_text(encoding='utf-8');smatches=list(BLOCK.finditer(stext))
                    check(path+'_matching_task_ids',{m[1] for m in smatches}==set(tblocks))
                    reconstructed=BLOCK.sub(lambda m:tblocks[m[1]],stext)
                    check(path+'_answer_substitution_exact',reconstructed==text)
                    pairs+=1
        check(level+'_task_count',len(level_ids)==count,str(len(level_ids)))
        check(level+'_unique_task_ids',len(set(level_ids))==len(level_ids))
        check(level+'_no_cross_level_duplicate',not (set(level_ids)&all_tasks));all_tasks.update(level_ids)
    for f in teacher.rglob('*.py'):
        ast.parse(f.read_text(encoding='utf-8'),filename=str(f))
        check(str(f.relative_to(teacher))+'_python_compile',True)
    texts=['실습 파일은 개인 폴더에 보관합니다.','프로젝트 폴더에서 서버를 실행합니다.','오류 메시지와 시도한 작업을 함께 적습니다.']
    check('seed_lengths',[len(x) for x in texts]==[20,20,24])
    check('seed_sum',sum(map(len,texts))==64)
    report.update(task_count=len(all_tasks),paired_sql_files=pairs,planned_execution_steps=step_count)
    report['passed']=all(x['passed'] for x in report['checks'])
    report['failed_checks']=[x for x in report['checks'] if not x['passed']]
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False,indent=2))
    return 0 if report['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
