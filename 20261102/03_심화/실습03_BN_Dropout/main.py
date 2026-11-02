from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent/'day11_image_classification'
sys.path.insert(0,str(PROJECT))
import torch
from torch import nn
import pandas as pd
from models import SmallCNN, build_model, set_training_mode
from data import load_data

torch.manual_seed(42)
torch.set_num_threads(1)
out=ROOT/'outputs';out.mkdir(exist_ok=True)

model=SmallCNN(batchnorm=True,dropout=0.3)
x=torch.rand(4,3,32,32)
model.train()
before=model.features[1].running_mean.clone()
y1,y2=model(x),model(x)
after=model.features[1].running_mean.clone()
# BEGIN D03
# TODO D03: 평가 모드로 바꾼 뒤 동일 입력 출력과 BN 상태를 확인한다.
model.train()
# END D03
with torch.no_grad():
    e1,e2=model(x),model(x)
print('train 출력 동일:',torch.equal(y1,y2))
print('BN 통계 변화:',not torch.equal(before,after))
print('eval 출력 동일:',torch.equal(e1,e2))
print('shape:',tuple(e1.shape))
