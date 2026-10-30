"""제공 코드: 독립 실행용 데이터·ANN·고정 epoch 학습. 상위 폴더를 import하지 않습니다."""
from pathlib import Path
import random,hashlib
import pandas as pd
import torch
from torch import nn
from torch.utils.data import TensorDataset,DataLoader

torch.set_num_threads(1)
BASE=Path(__file__).resolve().parent

def load_data():
    df=pd.read_csv(BASE/'data/points.csv')
    tr=df.loc[df.split=='train'].copy();va=df.loc[df.split=='valid'].copy()
    X=torch.tensor(tr[['x1','x2']].values,dtype=torch.float32)
    y=torch.tensor(tr.label.values,dtype=torch.long)
    Xv=torch.tensor(va[['x1','x2']].values,dtype=torch.float32)
    yv=torch.tensor(va.label.values,dtype=torch.long)
    ids={'train':tr.id.tolist(),'valid':va.id.tolist()}
    fingerprint=hashlib.sha256(pd.concat([tr,va]).to_csv(index=False).encode()).hexdigest()
    return X,y,Xv,yv,ids,fingerprint

def build_model(config):
    w=config.get('width',32);layers=[]
    for a,b in [(2,w),(w,w)]:
        layers.append(nn.Linear(a,b))
        if config.get('norm','none')=='batch': layers.append(nn.BatchNorm1d(b))
        elif config.get('norm','none')=='layer': layers.append(nn.LayerNorm(b))
        layers.extend([nn.ReLU(),nn.Dropout(config.get('dropout',0.))])
    layers.append(nn.Linear(w,2))
    return nn.Sequential(*layers)

def evaluate(model,X,y):
    modes=[(m,m.training) for m in model.modules()]
    try:
        model.eval()
        with torch.no_grad():
            logits=model(X)
            return float(nn.functional.cross_entropy(logits,y)),float((logits.argmax(1)==y).float().mean())
    finally:
        for m,flag in modes: m.training=flag

def fit_fixed(config, optimizer_factory=None, scheduler_factory=None, scheduler_step=None):
    # CPU 재현용. 각 후보마다 같은 초기화·배치 Generator를 다시 만듭니다.
    X,y,Xv,yv,ids,_=load_data()
    count=config.get('train_size',len(X));X,y=X[:count],y[:count]
    seed=config.get('seed',42);torch.manual_seed(seed);random.seed(seed)
    model=build_model(config)
    if optimizer_factory:
        optimizer=optimizer_factory(model.parameters(),config['optimizer'],config['lr'],config.get('weight_decay',0.))
    else:
        optimizer=torch.optim.AdamW(model.parameters(),lr=config.get('lr',.01),weight_decay=config.get('weight_decay',0.))
    epochs=config.get('epochs',20)
    scheduler=scheduler_factory(optimizer,config['scheduler'],epochs) if scheduler_factory else None
    loader=DataLoader(TensorDataset(X,y,torch.arange(len(y))),batch_size=config.get('batch_size',32),
        shuffle=True,generator=torch.Generator().manual_seed(seed+1),num_workers=0)
    history=[];traces=[]
    for epoch in range(1,epochs+1):
        model.train();seen=0;total=0.;trace=[];lr_used=optimizer.param_groups[0]['lr']
        for xb,yb,idx in loader:
            optimizer.zero_grad(set_to_none=True)
            loss=nn.functional.cross_entropy(model(xb),yb);loss.backward();optimizer.step()
            total+=loss.item()*len(yb);seen+=len(yb);trace.extend(idx.tolist())
        tl,ta=evaluate(model,X,y);vl,va=evaluate(model,Xv,yv)
        if scheduler: scheduler_step(scheduler,vl)
        history.append(dict(epoch=epoch,train_loss_step=total/seen,train_loss_eval=tl,valid_loss=vl,
                            train_acc=ta,valid_acc=va,lr_used=lr_used,lr_next=optimizer.param_groups[0]['lr']))
        traces.append(trace)
    return model,pd.DataFrame(history),traces
