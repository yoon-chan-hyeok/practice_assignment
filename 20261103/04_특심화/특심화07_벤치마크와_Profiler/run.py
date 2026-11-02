"""제공 실행기. 학습 대상은 tasks.py이며 이전 실습 파일은 필요 없다."""
from pathlib import Path
import json
import torch
from torch import nn
from support import init,write_json
from tasks import *
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'outputs'
OUT.mkdir(exist_ok=True)
init()

import argparse,pandas as pd
from models import classifier
parser=argparse.ArgumentParser();parser.add_argument('--profile',action='store_true');parser.add_argument('--device',default='cpu',choices=['cpu','cuda']);args=parser.parse_args()
if args.device=='cuda' and not torch.cuda.is_available():raise RuntimeError('명시한 CUDA 장치가 없습니다. CPU로 자동 위장하지 않습니다.')
device=torch.device(args.device);rows=[]
for name in ['RNN','LSTM','Transformer']:
    for length in [16,32,64]:
        init();model=classifier(name).to(device);x=torch.randn(4,length,3,device=device);lens=torch.tensor([length,length-3,length-6,length-9])
        for repeat in range(2):
            row=measure(model,x,lens,repeats=3,warmup=1,training=True)
            rows.append(dict(row,model=name,length=length,trial=repeat,batch=4,repeats=3,warmup=1))
pd.DataFrame(rows).to_csv(OUT/'timing_raw.csv',index=False)
pd.DataFrame(summarize_runs(rows)).to_csv(OUT/'timing_summary.csv',index=False)
print('모델3×길이3×반복2 =',len(rows),'행 / 동기화·구간·장치 기록 / CPU VRAM은 null')
if args.profile:
    from torch.profiler import profile,ProfilerActivity
    init();model=classifier('Transformer').to(device);cpu_x=torch.randn(4,16,3);lens=torch.tensor([16,12,10,8])
    activities=[ProfilerActivity.CPU]+([ProfilerActivity.CUDA] if device.type=='cuda' else [])
    with profile(activities=activities,record_shapes=True,profile_memory=True) as prof:
        loss=profile_workload(model,cpu_x,lens,device)
        if device.type=='cuda':torch.cuda.synchronize(device)
    prof.export_chrome_trace(str(OUT/'trace.json'))
    names={event.key for event in prof.key_averages()};required=['data.prepare','h2d','forward','backward']
    assert set(required)<=names
    write_json(OUT,'profiler_check.json',{'sections':required,'loss_finite':bool(torch.isfinite(torch.tensor(loss))),'device':str(device)})
    print('Profiler 구간 4개 기록 / CPU event 합계를 GPU 전체 지연으로 해석하지 않음')
