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

from models import classifier
from data import classification_data
from train import fit
data=classification_data(ROOT/"data"); rows=[]
for name in ["RNN","LSTM","Transformer"]:
    torch.manual_seed(42)
    # TODO D05: 후보 name에 해당하는 실제 아키텍처를 생성한다.
    # BEGIN D05
    model=classifier("LSTM")
    # END D05
    result=fit(model,data,"classification",epochs=25,lr=0.01)
    rows.append({"model":name,"params":result["params"],"best_epoch":result["best_epoch"],
                 "valid_loss":result["valid_loss"],"accuracy":result["valid_accuracy"]})
print(pd.DataFrame(rows).round(6).to_string(index=False))
pd.DataFrame(rows).to_csv(OUT/"architecture_comparison.csv",index=False)
