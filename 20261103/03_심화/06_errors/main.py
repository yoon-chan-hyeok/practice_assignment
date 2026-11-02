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
data=classification_data(ROOT/"data"); tables=[]; rows=[]
for name in ["RNN","LSTM","Transformer"]:
    torch.manual_seed(42); result=fit(classifier(name),data,"classification",epochs=25,lr=0.01)
    # TODO D06: 클래스 logits에서 실제 예측 라벨을 추출해 오류 행을 저장한다.
    # BEGIN D06
    pred=torch.zeros_like(data["valid"]["y"])
    # END D06
    actual=data["valid"]["y"]
    tables.extend({"model":name,"id":i,"actual":int(y),"prediction":int(p),"error":bool(y!=p)} for i,y,p in zip(data["valid"]["ids"],actual,pred))
    rows.append({"model":name,"params":result["params"],"seconds":result["seconds"],"valid_accuracy":result["valid_accuracy"]})
pd.DataFrame(tables).to_csv(OUT/"predictions.csv",index=False)
pd.DataFrame(rows).to_csv(OUT/"comparison.csv",index=False)
print(pd.DataFrame(tables).groupby("model")["error"].sum().to_string())
print("오류가 0이면 0건으로 기록한다. 오류 예시를 꾸며내지 않는다.")
