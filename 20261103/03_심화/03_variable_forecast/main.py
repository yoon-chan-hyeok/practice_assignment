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

from models import RecurrentModel
from data import forecast_data
from train import fit
data=forecast_data(ROOT/"data",variable=True); rows=[]
for use_packed in [False,True]:
    torch.manual_seed(42)
    # TODO D03: 후보의 packed 설정을 모델에 적용해 valid MSE를 비교한다.
    # BEGIN D03
    model=RecurrentModel("LSTM",packed=False)
    # END D03
    result=fit(model,data,epochs=30)
    rows.append({"packed":use_packed,"best_epoch":result["best_epoch"],"valid_mse":result["valid_loss"]})
print(pd.DataFrame(rows).round(6).to_string(index=False))
pd.DataFrame(rows).to_csv(OUT/"variable_comparison.csv",index=False)
print("dense는 마지막 Padding 상태를 쓰는 진단용 비교이며 권장 구현이 아니다.")
