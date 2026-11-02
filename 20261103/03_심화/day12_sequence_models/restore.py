import torch
from torch import nn
torch.set_num_threads(1)  # 작은 CPU 실습의 실행 조건을 고정한다.
torch.manual_seed(42)

from pathlib import Path
import pandas as pd
from models import RecurrentModel,Autoencoder,classifier
from data import forecast_data,reconstruction_data,classification_data
ROOT=Path(__file__).resolve().parent; OUT=ROOT/"outputs"
checkpoint=torch.load(OUT/"best_model.pt",map_location="cpu",weights_only=True)
rows=[]
for name in ["forecast","reconstruction","RNN","LSTM","Transformer"]:
    if name=="forecast": model=RecurrentModel("LSTM"); batch=forecast_data(ROOT/"data",True)["valid"]
    elif name=="reconstruction": model=Autoencoder(); batch=reconstruction_data(ROOT/"data")["valid"]
    else: model=classifier(name); batch=classification_data(ROOT/"data")["valid"]
    # TODO D10: 새로 만든 동일 구조 모델에 저장한 state_dict를 복원한다.
    # 본인이 생성한 신뢰하는 파일만 weights_only=True로 읽는다.
    # BEGIN D10
    pass
    # END D10
    model.eval()
    with torch.inference_mode(): output=model(batch["x"],batch["lengths"])
    if name=="forecast":
        old=pd.read_csv(OUT/"predictions.csv"); values=output.flatten()
        same_ids=old["time"].tolist()==batch["ids"]; reference=torch.tensor(old["prediction"].values,dtype=torch.float32)
    elif name=="reconstruction":
        old=pd.read_csv(OUT/"reconstruction.csv"); values=((output-batch["y"])**2).mean(1)
        same_ids=old["end_time"].tolist()==batch["ids"]; reference=torch.tensor(old["mse"].values,dtype=torch.float32)
    else:
        old=pd.read_csv(OUT/"classification_predictions.csv"); old=old[old["model"]==name]
        values=output.argmax(1).float(); same_ids=old["id"].tolist()==batch["ids"]; reference=torch.tensor(old["prediction"].values,dtype=torch.float32)
    rows.append({"model":name,"ids_equal":same_ids,"values_equal":torch.allclose(values,reference,atol=1e-6,rtol=1e-5)})
pd.DataFrame(rows).to_csv(OUT/"restore_check.csv",index=False)
print(pd.DataFrame(rows).to_string(index=False))
