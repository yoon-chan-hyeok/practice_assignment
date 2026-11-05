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
for frozen in [True,False]:
    # TODO D02: freeze_bn에 현재 frozen을 전달하세요.
    # BEGIN D02
    model,summary,history,prediction=experiment(DATA,freeze_bn=True,epochs=6)  # frozen 값을 전달하세요.
    # END D02
    source=build_model(DATA)
    summary["freeze_bn"]=frozen
    summary["bn_shift"]=(model[1].running_mean-source[1].running_mean).abs().max().item()
    rows.append(summary)
table=pd.DataFrame(rows);table.to_csv(OUT/"bn_policy.csv",index=False)
print(table[["freeze_bn","accuracy","macro_f1","bn_shift"]].round(4).to_string(index=False))
