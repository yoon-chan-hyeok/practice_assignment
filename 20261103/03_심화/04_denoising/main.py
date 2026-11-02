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

from models import Autoencoder
from data import reconstruction_data
from train import fit
# TODO D04: 입력만 노이즈를 더하고 정답은 깨끗한 Window로 유지한다.
# BEGIN D04
data=reconstruction_data(ROOT/"data",noisy=False)
# END D04
model=Autoencoder(8,4); result=fit(model,data,epochs=40)
valid=data["valid"]
noisy_mse=nn.MSELoss()(valid["x"],valid["y"]).item()
print("노이즈 입력 자체 MSE:",round(noisy_mse,6))
print("재구성 MSE:",round(result["valid_loss"],6),"best epoch:",result["best_epoch"])
pd.DataFrame({"end_time":valid["ids"],"input_mse":((valid["x"]-valid["y"])**2).mean(1).tolist(),
              "reconstruction_mse":((result["prediction"]-valid["y"])**2).mean(1).tolist()}).to_csv(OUT/"denoising.csv",index=False)
print("작은 모델이 입력보다 더 나쁘게 복원할 수도 있다. 개선을 가정하지 않는다.")
