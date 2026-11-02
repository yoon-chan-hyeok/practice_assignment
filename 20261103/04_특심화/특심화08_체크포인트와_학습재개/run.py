"""자체적으로 4epoch 연속 / 2epoch 중단 / 새 프로세스 4epoch 재개를 실행한다."""
from pathlib import Path
import subprocess,sys,json,os
import torch
from support import identical,write_json
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'outputs';OUT.mkdir(exist_ok=True)
if __name__=='__main__':
    env=dict(os.environ,OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',PYTHONUTF8='1')
    jobs=[['--epochs','4','--output','outputs/full'],['--epochs','2','--output','outputs/part'],
          ['--epochs','4','--output','outputs/resumed','--resume','outputs/part/checkpoint.pt']]
    for job in jobs:
        p=subprocess.run([sys.executable,str(ROOT/'resume_train.py'),*job],cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',timeout=90)
        if p.returncode:raise RuntimeError(p.stdout+'\n'+p.stderr)
        print(p.stdout.strip())
    a=torch.load(OUT/'full/checkpoint.pt',weights_only=True);b=torch.load(OUT/'resumed/checkpoint.pt',weights_only=True)
    result={k:identical(a[k],b[k]) for k in a}
    write_json(OUT,'resume_check.json',result)
    if not all(result.values()):raise AssertionError('resume mismatch')
    print('저장 상태',len(result),'범주 일치 / CPU·동일 버전·epoch 경계·num_workers=0')
