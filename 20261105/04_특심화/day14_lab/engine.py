"""제공되는 학습·평가 골격. train/valid만 모델에 전달하고 test는 열지 않습니다."""
from pathlib import Path
import time,copy
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader,WeightedRandomSampler
from torchvision import transforms as T
from torchvision.datasets import ImageFolder
from sklearn.metrics import accuracy_score,f1_score,classification_report,confusion_matrix
from models import build_model,configure,training_mode


def datasets(data):
    transform=T.Compose([T.Resize((32,32)),T.ToTensor()])
    return (ImageFolder(Path(data)/'train',transform),ImageFolder(Path(data)/'valid',transform))


def metrics(y,prob):
    pred=prob.argmax(1)
    report=classification_report(y,pred,labels=[0,1,2],output_dict=True,zero_division=0)
    return {'accuracy':float(accuracy_score(y,pred)),
            'macro_f1':float(f1_score(y,pred,labels=[0,1,2],average='macro',zero_division=0)),
            'circle_recall':report['0']['recall'],'square_recall':report['1']['recall'],'triangle_recall':report['2']['recall']}


def evaluate(model,loader):
    """평가 손실은 가중치 없이 계산합니다. 모든 행을 한 번씩 평가하고 표본 수로 집계합니다."""
    flags=[(m,m.training) for m in model.modules()]
    model.eval();ys=[];ps=[];total=0.;n=0
    with torch.no_grad():
        for x,y in loader:
            logits=model(x);total+=nn.functional.cross_entropy(logits,y,reduction='sum').item();n+=len(y)
            ys.extend(y.tolist());ps.append(logits.softmax(1).cpu())
    for m,flag in flags:m.training=flag
    prob=torch.cat(ps).numpy();summary=metrics(np.array(ys),prob);summary['loss']=total/n
    return summary,np.array(ys),prob


def experiment(data, strategy='head', balance='none', epochs=8, seed=14, freeze_bn=True, pretrained=True, switch_epoch=None):
    """같은 분할·예산을 비교합니다. 모든 후보의 valid는 동일한 비가중 평가입니다."""
    if balance not in {'none','weight','sampler'}:raise ValueError('unknown balance')
    torch.set_num_threads(1);train,valid=datasets(data)
    model=build_model(data,pretrained,seed);optimizer=configure(model,strategy,head_lr=.01,backbone_lr=.001)
    g=torch.Generator().manual_seed(seed)
    counts=torch.bincount(torch.tensor(train.targets),minlength=3).float()
    class_weights=(1/counts);class_weights/=class_weights.mean()
    sampler=WeightedRandomSampler((1/counts)[train.targets],len(train),replacement=True,generator=g) if balance=='sampler' else None
    loader=DataLoader(train,batch_size=16,shuffle=sampler is None,sampler=sampler,generator=g,num_workers=0)
    vl=DataLoader(valid,batch_size=32,shuffle=False,num_workers=0)
    loss_fn=nn.CrossEntropyLoss(weight=class_weights if balance=='weight' else None)
    best=float('inf');history=[];best_state=None;seen=[]
    start=time.perf_counter()
    for epoch in range(1,epochs+1):
        if switch_epoch is not None and epoch==switch_epoch:
            # 교육용 순차 비교: 옵티마이저 재생성 → 기존 momentum이 초기화됨을 보고서에 명시.
            optimizer=configure(model,'partial',head_lr=.01,backbone_lr=.001)
        training_mode(model,freeze_bn)
        numerator=0.;denominator=0.;sample_counts=torch.zeros(3,dtype=torch.long)
        for x,y in loader:
            optimizer.zero_grad(set_to_none=True);logits=model(x)
            loss=loss_fn(logits,y);loss.backward();optimizer.step()
            denom=float(class_weights[y].sum()) if balance=='weight' else len(y)
            numerator+=loss.item()*denom;denominator+=denom;sample_counts+=torch.bincount(y,minlength=3)
        summary,_,_=evaluate(model,vl)
        history.append({'epoch':epoch,'strategy':strategy,'balance':balance,'train_objective':numerator/denominator,'valid_loss':summary['loss'],'valid_macro_f1':summary['macro_f1'],'draw_circle':int(sample_counts[0]),'draw_square':int(sample_counts[1]),'draw_triangle':int(sample_counts[2])})
        if summary['loss']<best:
            best=summary['loss'];best_epoch=epoch;best_state=copy.deepcopy(model.state_dict())
    seconds=time.perf_counter()-start
    model.load_state_dict(best_state);model.eval()
    summary,y,prob=evaluate(model,vl)
    summary.update({'strategy':strategy,'balance':balance,'best_epoch':best_epoch,'trainable':sum(p.numel() for p in model.parameters() if p.requires_grad),'epochs':epochs,'seconds':seconds,'source':'synthetic_source' if pretrained else 'scratch'})
    prediction=pd.DataFrame({'path':[str(Path(p).relative_to(data)) for p,_ in valid.samples], 'actual':y,'predicted':prob.argmax(1),'confidence':prob.max(1)})
    for i in range(3):prediction[f'p{i}']=prob[:,i]
    return model,summary,pd.DataFrame(history),prediction
