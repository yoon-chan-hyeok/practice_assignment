"""제공 실행기. 학습 대상은 tasks.py이며 이전 실습 파일은 필요 없다."""
from pathlib import Path
import json
import torch
from torch import nn
from support import init,write_json
from tasks import *
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'outputs'
OUT.mkdir(exist_ok=True)
init()

import pandas as pd
from copy import deepcopy
from time import perf_counter
from torch.utils.data import DataLoader,TensorDataset
from data import classification_data
from models import classifier
d=classification_data(ROOT/'data');tr=d['train'];va=d['valid']
loader=DataLoader(TensorDataset(va['x'],va['lengths'],va['y'],torch.arange(len(va['y']))),batch_size=7,shuffle=False)
rows=[];predictions=[];history=[]
for name in ['RNN','LSTM','Transformer']:
    init();model=classifier(name);optimizer=torch.optim.Adam(model.parameters(),lr=.01);best=float('inf');start=perf_counter()
    for epoch in range(1,16):
        model.train();optimizer.zero_grad(set_to_none=True)
        loss=nn.CrossEntropyLoss()(model(tr['x'],tr['lengths']),tr['y']);loss.backward();optimizer.step()
        score=evaluate_batches(model,loader)
        history.append({'model':name,'epoch':epoch,'valid_loss':score['loss']})
        if score['loss']<best:best=score['loss'];state=deepcopy(model.state_dict());best_epoch=epoch
    seconds=perf_counter()-start;model.load_state_dict(state)
    score=evaluate_batches(model,loader);check=check_padding_invariance(model,va['x'],va['lengths'])
    rows.append({'model':name,'params':sum(p.numel() for p in model.parameters()),'best_epoch':best_epoch,'valid_loss':score['loss'],
                 'accuracy':score['accuracy'],'padding_invariant':check['unchanged'],'seconds':seconds})
    predictions.extend({'model':name,'id':va['ids'][i],'actual':y,'prediction':p} for i,y,p in zip(score['ids'],score['targets'],score['predictions']))
pd.DataFrame(rows).to_csv(OUT/'comparison.csv',index=False);pd.DataFrame(history).to_csv(OUT/'history.csv',index=False)
pd.DataFrame(predictions).to_csv(OUT/'predictions.csv',index=False)
print(pd.DataFrame(rows).drop(columns='seconds').round(6).to_string(index=False));print('동일 train60/valid20·15epochs / 모델 크기는 기록하며 동일하다고 주장하지 않음 / test 미사용')
