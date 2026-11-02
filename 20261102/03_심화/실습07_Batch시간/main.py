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

from train import benchmark
from torch.utils.data import DataLoader
train,_,_,_,_,_=load_data()
# BEGIN D07
# TODO D07: Batch 8·16·32를 동일 모델·자료 순서로 비교한다.
batches=[8]
# END D07
base=SmallCNN()
rows=[]
for device_name in ['cpu']+(['cuda'] if torch.cuda.is_available() else []):
    for batch in batches:
        loader=DataLoader(train,batch_size=batch,shuffle=False,num_workers=0)
        rows.extend(benchmark(base,loader,torch.device(device_name),repeats=2))
pd.DataFrame(rows).to_csv(out/'batch_benchmark.csv',index=False)
print(pd.DataFrame(rows).round(3).to_string(index=False))
if not torch.cuda.is_available(): print('CUDA 비교: N/A')
