import torch
from torch import nn
torch.set_num_threads(1)  # 작은 CPU 실습의 실행 조건을 고정한다.
torch.manual_seed(42)

from pathlib import Path
import pandas as pd
from models import RecurrentModel, Autoencoder, classifier
from data import forecast_data,reconstruction_data,classification_data
from train import fit
ROOT=Path(__file__).resolve().parent; OUT=ROOT/"outputs"; OUT.mkdir(exist_ok=True)
forecast_batches=forecast_data(ROOT/"data",variable=True)
forecast=RecurrentModel("LSTM")
# TODO D08: 제공된 fit으로 LSTM 예측 모델을 학습하고 best 결과를 받는다.
# BEGIN D08
forecast_result=None
# END D08
ae_batches=reconstruction_data(ROOT/"data"); torch.manual_seed(42); ae=Autoencoder()
# TODO D09: Autoencoder를 입력 재구성 문제로 학습한다. forecast y와 섞지 않는다.
# BEGIN D09
ae_result=None
# END D09
classification_batches=classification_data(ROOT/"data")
results={"forecast":forecast_result,"reconstruction":ae_result}
for name in ["RNN","LSTM","Transformer"]:
    torch.manual_seed(42); results[name]=fit(classifier(name),classification_batches,"classification",epochs=25,lr=0.01)
summary=[]; histories=[]; states={}
for name,result in results.items():
    summary.append({"task":name,"params":result["params"],"best_epoch":result["best_epoch"],"valid_loss":result["valid_loss"],
                    "valid_accuracy":result["valid_accuracy"],"seconds":result["seconds"]})
    histories.extend(dict(task=name,**row) for row in result["history"])
    states[name]=result["state"]
pd.DataFrame(summary).to_csv(OUT/"architecture_comparison.csv",index=False)
pd.DataFrame(histories).to_csv(OUT/"history.csv",index=False)
val=forecast_batches["valid"]
pd.DataFrame({"time":val["ids"],"actual":val["y"].flatten().tolist(),"prediction":forecast_result["prediction"].flatten().tolist()}).to_csv(OUT/"predictions.csv",index=False)
val=ae_batches["valid"]
pd.DataFrame({"end_time":val["ids"],"mse":((ae_result["prediction"]-val["y"])**2).mean(1).tolist()}).to_csv(OUT/"reconstruction.csv",index=False)
val=classification_batches["valid"]; prediction_rows=[]
for name in ["RNN","LSTM","Transformer"]:
    logits=results[name]["prediction"]
    prediction_rows.extend({"model":name,"id":i,"actual":int(y),"prediction":int(p)} for i,y,p in zip(val["ids"],val["y"],logits.argmax(1)))
pd.DataFrame(prediction_rows).to_csv(OUT/"classification_predictions.csv",index=False)
torch.save({"states":states,"forecast_variable":True,"lookback":12,"ae_features":8,"schema":1},OUT/"best_model.pt")
print(pd.DataFrame(summary).drop(columns="seconds").round(6).to_string(index=False))
print("test 구간/ID: 모델에 전달하지 않음")
# 그래프는 재구성 한 건만 표시한다. 별도 figure에 그린다.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.figure(figsize=(7,4)); plt.plot(ae_batches["valid"]["y"][0].tolist(),label="Input",marker="o")
plt.plot(ae_result["prediction"][0].tolist(),label="Reconstruction",marker="s")
plt.xlabel("Position"); plt.ylabel("Signal"); plt.legend(); plt.tight_layout()
plt.savefig(OUT/"mask_or_latent.png",dpi=120); plt.close()
