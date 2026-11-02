"""세 개의 새 프로세스로 연속/중단/재개를 수행한다. 임의 인터넷 checkpoint를 읽지 않는다."""
import os,subprocess,sys
import torch
from tasks import compare_states
from support import ROOT,save_json

def main():
    out=ROOT/'outputs';out.mkdir(exist_ok=True)
    env=dict(os.environ,OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
    commands=[['--epochs','4','--out',str(out/'continuous')],
              ['--epochs','4','--stop-after','2','--out',str(out/'split')],
              ['--epochs','4','--resume',str(out/'split/checkpoint.pt'),'--out',str(out/'resumed')]]
    for args in commands:
        run=subprocess.run([sys.executable,str(ROOT/'worker.py'),*args],env=env,capture_output=True,text=True,timeout=120)
        if run.returncode: raise RuntimeError(run.stderr+run.stdout)
        print(run.stdout.strip())
    a=torch.load(out/'continuous/checkpoint.pt',map_location='cpu',weights_only=True)
    b=torch.load(out/'resumed/checkpoint.pt',map_location='cpu',weights_only=True)
    differences=compare_states(a,b)
    report=dict(equal=not differences,checked_keys=sorted(a),mismatches=differences,epochs=4,split_at=2,
                scope='same CPU/version/threads=1/workers=0/epoch boundary')
    save_json('resume_comparison.json',report)
    assert not differences,differences
    print('4회 연속 vs 2+새 프로세스+2 전체 상태 일치:',not differences)
if __name__=='__main__': main()
