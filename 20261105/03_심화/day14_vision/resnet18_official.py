"""공식 ImageNet ResNet18 선택 경로. 실행: python resnet18_official.py --strategy head
공식 가중치가 없으면 실제 오류를 내며, weights=None으로 자동 대체하지 않습니다.
"""
from pathlib import Path
import argparse,json,time,copy
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torchvision.models import resnet18,ResNet18_Weights
from sklearn.metrics import accuracy_score,f1_score


def main():
    p=argparse.ArgumentParser();p.add_argument('--strategy',choices=['head','partial'],default='head');p.add_argument('--epochs',type=int,default=2);a=p.parse_args()
    torch.set_num_threads(1);torch.manual_seed(14)
    base=Path(__file__).resolve().parent;data=base/'data';out=base/'outputs'/'imagenet';out.mkdir(parents=True,exist_ok=True)
    weights=ResNet18_Weights.IMAGENET1K_V1
    model=resnet18(weights=weights)  # 공식 다운로드 또는 공식 캐시. 실패 시 여기서 중단.
    for param in model.parameters():param.requires_grad_(False)
    model.fc=nn.Linear(model.fc.in_features,3)
    groups=[{'params':list(model.fc.parameters()),'lr':.001}]
    if a.strategy=='partial':
        for param in model.layer4.parameters():param.requires_grad_(True)
        groups.append({'params':list(model.layer4.parameters()),'lr':.0001})
    device=torch.device('cuda' if torch.cuda.is_available() else 'cpu');model.to(device)
    transform=weights.transforms()  # RGB / Resize256 / CenterCrop224 / ImageNet Normalize
    train=ImageFolder(data/'train',transform);valid=ImageFolder(data/'valid',transform)
    g=torch.Generator().manual_seed(14)
    tl=DataLoader(train,batch_size=8,shuffle=True,generator=g,num_workers=0);vl=DataLoader(valid,batch_size=8,shuffle=False,num_workers=0)
    opt=torch.optim.AdamW(groups,weight_decay=.0001);criterion=nn.CrossEntropyLoss();history=[];best=float('inf')
    for epoch in range(1,a.epochs+1):
        model.train()
        for module in model.modules():
            if isinstance(module,nn.BatchNorm2d):module.eval()  # 동결/부분학습 모두 BN 통계 고정
        for x,y in tl:
            x=x.to(device);y=y.to(device);opt.zero_grad(set_to_none=True);loss=criterion(model(x),y);loss.backward();opt.step()
        model.eval();ys=[];preds=[];total=0
        with torch.no_grad():
            for x,y in vl:
                x=x.to(device);yy=y.to(device);logits=model(x);total+=nn.functional.cross_entropy(logits,yy,reduction='sum').item();ys.extend(y.tolist());preds.extend(logits.argmax(1).cpu().tolist())
        result={'epoch':epoch,'valid_loss':total/len(valid),'accuracy':accuracy_score(ys,preds),'macro_f1':f1_score(ys,preds,labels=[0,1,2],average='macro',zero_division=0)};history.append(result)
        if result['valid_loss']<best:best=result['valid_loss'];state={k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
    torch.save({'model':state,'class_to_idx':train.class_to_idx,'weights':'IMAGENET1K_V1','transform':str(transform),'strategy':a.strategy},out/(a.strategy+'.pt'))
    (out/(a.strategy+'.json')).write_text(json.dumps({'history':history,'source':'ImageNet','strategy':a.strategy,'test_used':False},indent=2),encoding='utf-8')
    print(json.dumps(history[-1],sort_keys=True))

if __name__=='__main__':main()
