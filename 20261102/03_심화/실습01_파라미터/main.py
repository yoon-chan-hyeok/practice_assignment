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

mlp=nn.Linear(3*32*32,64)
conv=nn.Conv2d(3,64,3,padding=1)
rows=[]
for name,model in [('Linear',mlp),('Conv2d',conv)]:
    # BEGIN D01
    # TODO D01: 모든 파라미터 원소 수를 더한다.
    count=0
    # END D01
    rows.append(dict(model=name,parameters=count))
print(pd.DataFrame(rows).to_string(index=False))
pd.DataFrame(rows).to_csv(out/'parameters.csv',index=False)
