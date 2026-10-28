"""개별 실습 실행 후 수치·파일을 예상 결과와 비교합니다. 보고서 문장은 채점하지 않습니다.
예: python tools/check_practice.py --exercise 4 --level basic
"""
from pathlib import Path
import os,sys,argparse,subprocess,json
os.environ.setdefault('OMP_NUM_THREADS','1');os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
LEVELS={'basic':'01_기본필수','applied':'02_응용','advanced':'03_심화'}
SKIP={'evaluation_lock.json','evaluation_receipt.json','experiment_plan.json','evaluation_lock.sha256'}

def compare_value(actual,expected,where=''):
    if isinstance(expected,dict):
        for k,v in expected.items():
            if k not in actual:raise AssertionError(f'{where}: 키 누락 {k}')
            compare_value(actual[k],v,where+'/'+str(k))
    elif isinstance(expected,list):
        if len(actual)!=len(expected):raise AssertionError(where+': 길이 불일치')
        for i,(a,b) in enumerate(zip(actual,expected)):compare_value(a,b,where+f'/{i}')
    elif isinstance(expected,(float,int)) and not isinstance(expected,bool):
        if not np.isclose(actual,expected,rtol=1e-7,atol=1e-9,equal_nan=True):raise AssertionError(where+': 수치 불일치')
    elif actual!=expected:raise AssertionError(where+': 값 불일치')

def check_step(number,level):
    folder=next(ROOT.glob(f'ex{number:02d}_*'))/LEVELS[level]
    result=subprocess.run([sys.executable,str(folder/'main.py')],cwd=ROOT,capture_output=True,text=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    checks=0
    for expected in sorted((folder/'expected_outputs').glob('*')):
        if expected.name in SKIP or expected.suffix not in ['.json','.csv']:continue
        actual=folder/'outputs'/expected.name
        if not actual.exists():raise AssertionError('출력 누락: '+actual.name)
        if expected.suffix=='.json':compare_value(json.loads(actual.read_text(encoding='utf-8')),json.loads(expected.read_text(encoding='utf-8')),actual.name)
        else:
            a=pd.read_csv(actual);b=pd.read_csv(expected)
            pd.testing.assert_frame_equal(a,b,check_dtype=False,check_exact=False,rtol=1e-7,atol=1e-9)
        checks+=1
    return checks

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--exercise',type=int,choices=range(1,7));p.add_argument('--level',choices=LEVELS,default='basic');p.add_argument('--all',action='store_true');a=p.parse_args()
    targets=[(n,l) for n in range(1,7) for l in LEVELS] if a.all else [(a.exercise,a.level)] if a.exercise else []
    if not targets:p.error('--exercise N 또는 --all을 지정하세요. 실습07/08은 day8_final의검사명령을사용합니다.')
    errors=[];total=0
    for n,l in targets:
        try:
            count=check_step(n,l);total+=count;print(f'PASS ex{n:02d}/{l}: {count}개 출력 확인',flush=True)
        except Exception as exc:
            errors.append((n,l,str(exc)));print(f'FAIL ex{n:02d}/{l}: {exc}',flush=True)
    print(f'실행 {len(targets)}건 / 실패 {len(errors)}건 / 확인 출력 {total}개')
    if errors:sys.exit(1)
if __name__=='__main__':main()
