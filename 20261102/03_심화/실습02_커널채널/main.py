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

x=torch.rand(4,3,32,32)
rows=[]
for channels,kernel in [(8,3),(16,3),(8,5)]:
    # BEGIN D02
    # TODO D02: 현재 channels와 kernel을 사용해 층을 만든다.
    layer=nn.Conv2d(3,8,3,padding=1)
    # END D02
    y=layer(x)
    rows.append(dict(channels=channels,kernel=kernel,shape=str(tuple(y.shape)),parameters=sum(p.numel() for p in layer.parameters())))
print(pd.DataFrame(rows).to_string(index=False))
pd.DataFrame(rows).to_csv(out/'kernels.csv',index=False)
