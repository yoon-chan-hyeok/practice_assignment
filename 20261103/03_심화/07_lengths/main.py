import torch
from torch import nn
torch.set_num_threads(1)  # 작은 CPU 실습의 실행 조건을 고정한다.
torch.manual_seed(42)
from pathlib import Path
import sys
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"day12_sequence_models"))  # 제공 모듈의 위치; 수정하지 않는다.
OUT=Path(__file__).resolve().parent/"outputs"
OUT.mkdir(exist_ok=True)

from time import perf_counter
from models import classifier
rows=[]
for length in [16,32,64]:
    for name in ["RNN","LSTM","Transformer"]:
        torch.manual_seed(42); model=classifier(name).eval(); x=torch.randn(16,length,3); lengths=torch.full((16,),length)
        with torch.inference_mode():
            for _ in range(3): model(x,lengths)
            start=perf_counter()
            for _ in range(20): model(x,lengths)
            elapsed=perf_counter()-start
        # TODO D07: 실제로 측정한 20회 전체의 샘플 수로 throughput을 계산한다.
        # BEGIN D07
        samples_s=16/elapsed
        # END D07
        rows.append({"model":name,"length":length,"seconds":elapsed,"samples_s":samples_s,"device":"cpu","peak_vram":None})
pd.DataFrame(rows).to_csv(OUT/"lengths.csv",index=False)
print(pd.DataFrame(rows).to_string(index=False))
print("측정: CPU 순전파 / 워밍업 제외 / 배치16 / 반복20 / GPU VRAM 미측정")
