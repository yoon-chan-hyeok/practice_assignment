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
for plan in ["partial_from_start","head_then_partial"]:
    strategy="partial" if plan=="partial_from_start" else "head"
    # TODO D03: head_then_partial은 epoch 5부터 partial을 시작하세요(총 8회).
    # BEGIN D03
    switch=None  # 순차 계획일 때 5를 선택하세요.
    # END D03
    _,summary,history,_=experiment(DATA,strategy=strategy,epochs=8,switch_epoch=switch)
    summary["plan"]=plan;rows.append(summary)
    history.to_csv(OUT/f"{plan}_history.csv",index=False)
print(pd.DataFrame(rows)[["plan","accuracy","macro_f1","best_epoch"]].round(4).to_string(index=False))
print("epoch 5에서 optimizer 재구성: Head의 이전 적응 상태 초기화. 같은 총 8회 예산 비교.")
pd.DataFrame(rows).to_csv(OUT/"stage_comparison.csv",index=False)
