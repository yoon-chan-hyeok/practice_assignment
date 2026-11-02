import torch
from torch import nn
torch.set_num_threads(1)  # 작은 CPU 실습의 실행 조건을 고정한다.
torch.manual_seed(42)
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"outputs"
OUT.mkdir(exist_ok=True)

from copy import deepcopy
from time import perf_counter
base=nn.LSTM(3,8,batch_first=True).eval(); x_cpu=torch.randn(16,12,3); rows=[]
for name in ["cpu","cuda"]:
    if name=="cuda" and not torch.cuda.is_available():
        rows.append({"device":"cuda","status":"NOT_AVAILABLE","seconds":None,"samples_s":None,"peak_bytes":None})
        continue
    device=torch.device(name); model=deepcopy(base).to(device); x=x_cpu.to(device)
    with torch.inference_mode():
        for _ in range(5): model(x)
        if device.type=="cuda":
            torch.cuda.synchronize(device); torch.cuda.reset_peak_memory_stats(device)
        start=perf_counter()
        for _ in range(30): model(x)
        # TODO A07: CUDA 측정 종료 전에 비동기 작업의 완료를 기다린다.
        # CPU에는 synchronize를 호출하지 않는다. 시작 직전 동기화는 제공되어 있다.
        # BEGIN A07
        pass
        # END A07
        elapsed=perf_counter()-start
    peak=torch.cuda.max_memory_allocated(device) if device.type=="cuda" else None
    rows.append({"device":name,"status":"OK","seconds":elapsed,"samples_s":480/elapsed,"peak_bytes":peak})
pd.DataFrame(rows).to_csv(OUT/"device_time.csv",index=False)
print(pd.DataFrame(rows).to_string(index=False))
print("동일 초기상태·입력 / forward 30회 / H2D·DataLoader·backward 제외 / VRAM=모델+입력 포함 allocated peak")
