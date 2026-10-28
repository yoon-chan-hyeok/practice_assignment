"""제공 실행기: 별도 프로젝트를 만들지 않고 day8_final을 이어서 사용합니다."""
from pathlib import Path
import subprocess,sys,os
os.environ.setdefault('OMP_NUM_THREADS','1');os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'day8_final').is_dir())
PROJECT=ROOT/'day8_final'
if __name__=='__main__':
    subprocess.run([sys.executable,str(PROJECT/'main.py')]+[],cwd=PROJECT,check=True)
    subprocess.run([sys.executable,str(PROJECT/'test_cases.py')]+[],cwd=PROJECT,check=True)
