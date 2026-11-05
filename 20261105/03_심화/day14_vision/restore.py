from pathlib import Path
import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader
from engine import datasets,evaluate
from models import build_model
BASE=Path(__file__).resolve().parent;DATA=BASE/"data";OUT=BASE/"outputs"
torch.set_num_threads(1)
# 직접 생성한 파일만 읽습니다. 임의 출처의 직렬화 파일을 로드하지 않습니다.
saved=torch.load(OUT/"best_model.pt",map_location="cpu",weights_only=True)
model=build_model(DATA)
# TODO D10: model.load_state_dict로 저장 가중치를 복원하세요.
# BEGIN D10
pass  # 저장 모델 가중치를 적용하세요.
# END D10
model.eval();_,valid=datasets(DATA)
summary,y,prob=evaluate(model,DataLoader(valid,batch_size=32,shuffle=False))
expected=pd.read_csv(OUT/"predictions.csv")
paths=[str(Path(p).relative_to(DATA)) for p,_ in valid.samples]
print("ID 순서:",paths==expected.path.tolist())
print("확률 일치:",np.allclose(prob,expected[["p0","p1","p2"]].to_numpy(),atol=1e-6,rtol=1e-5))
print("예측 일치:",np.array_equal(prob.argmax(1),expected.predicted.to_numpy()))
