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

# 전이 모델은 실제 사전학습 가중치를 사용한다. 없으면 다운로드하며 무작위 대체하지 않는다.
# BEGIN D06
# TODO D06: SmallCNN·Head·Partial 세 경로를 실행한다.
SETTINGS=[('small',16,1)]
# END D06

from models import set_training_mode
from train import evaluate
import copy,time
rows=[]
for kind,width,epochs in SETTINGS:
    torch.manual_seed(42)
    train,_,valid,loader,train_check,valid_loader=load_data(kind,batch_size=16 if kind=='small' else 4)
    model=build_model(kind,width=width)
    if kind=='partial':
        groups=[{'params':model.fc.parameters(),'lr':0.001},{'params':model.layer4.parameters(),'lr':0.0001}]
    elif kind=='head': groups=model.fc.parameters()
    else: groups=model.parameters()
    optimizer=torch.optim.AdamW(groups,lr=0.01 if kind=='small' else 0.001,weight_decay=0.0001)
    history=[];best=float('inf');start=time.perf_counter()
    for epoch in range(1,epochs+1):
        set_training_mode(model,kind)
        for x,y in loader:
            optimizer.zero_grad(set_to_none=True)
            nn.functional.cross_entropy(model(x),y).backward();optimizer.step()
        tl,ta,_,_=evaluate(model,train_check,torch.device('cpu'))
        vl,va,_,_=evaluate(model,valid_loader,torch.device('cpu'))
        history.append(dict(epoch=epoch,train_loss=tl,valid_loss=vl,train_accuracy=ta,valid_accuracy=va))
        if vl<best: best=vl;best_epoch=epoch;best_state=copy.deepcopy(model.state_dict())
    seconds=time.perf_counter()-start
    model.load_state_dict(best_state)
    vl,va,_,_=evaluate(model,valid_loader,torch.device('cpu'))
    name=f'{kind}_w{width}'
    pd.DataFrame(history).to_csv(out/f'history_{name}.csv',index=False)
    rows.append(dict(model=name,trainable_params=sum(p.numel() for p in model.parameters() if p.requires_grad),
                     image_size=32 if kind=='small' else 224,epochs=epochs,best_epoch=best_epoch,
                     valid_loss=vl,valid_accuracy=va,training_seconds=seconds,
                     source_weights='none' if kind=='small' else 'IMAGENET1K_V1'))
    print(name,'best',best_epoch,'valid loss',round(vl,4),'accuracy',round(va,4))
pd.DataFrame(rows).to_csv(out/'comparison.csv',index=False)

print('small32/ResNet224·배치16/4·학습률의 차이가 있으므로 학습 전략 전체의 비교이다.')
