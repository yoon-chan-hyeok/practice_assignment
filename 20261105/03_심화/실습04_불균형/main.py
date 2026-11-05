from pathlib import Path
import sys,json
import numpy as np
import pandas as pd
import torch
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE.parent/"day14_vision"))
DATA=BASE.parent/"data"
OUT=BASE/"outputs"
OUT.mkdir(exist_ok=True)
torch.set_num_threads(1)
from engine import experiment,datasets,metrics
from models import build_model,configure

rows=[]
# TODO D04: none, weight, sampler를 각각 독립 후보로 비교하세요. 동시에 적용하지 않습니다.
# BEGIN D04
methods=["none"]  # weight와 sampler를 별개 후보로 추가하세요.
# END D04
for method in methods:
    _,summary,history,_=experiment(DATA,balance=method,epochs=8)
    rows.append(summary);history.to_csv(OUT/f"{method}_history.csv",index=False)
result=pd.DataFrame(rows);result.to_csv(OUT/"imbalance_comparison.csv",index=False)
print(result[["balance","accuracy","macro_f1","triangle_recall"]].round(4).to_string(index=False))
print("sampler는 train만 재추출합니다. valid는 원래 분포 그대로입니다.")
