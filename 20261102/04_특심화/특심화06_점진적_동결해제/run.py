import argparse,copy
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.models import resnet18,ResNet18_Weights
from tasks import configure_transfer,trainable_report
from support import ROOT,seed_all,save_json

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--pretrained',action='store_true')
    args=parser.parse_args();seed_all()
    weights=ResNet18_Weights.IMAGENET1K_V1 if args.pretrained else None
    model=resnet18(weights=weights);model.fc=nn.Linear(model.fc.in_features,2)
    if weights is None:
        batches=[(torch.rand(2,3,32,32),torch.tensor([0,1]))]
    else:
        ds=datasets.ImageFolder(ROOT/'data/train',transform=weights.transforms())
        batches=DataLoader(ds,batch_size=4,shuffle=False,num_workers=0)
    optimizer=None;rows=[];out=ROOT/'outputs';out.mkdir(exist_ok=True)
    for stage in ('head','partial'):
        optimizer=configure_transfer(model,stage,optimizer);report=trainable_report(model,optimizer)
        before=copy.deepcopy(model.state_dict())
        for x,y in batches:
            optimizer.zero_grad(set_to_none=True);nn.functional.cross_entropy(model(x),y).backward();optimizer.step()
        changed=[n for n,p in model.named_parameters() if not torch.equal(p,before[n])]
        assert all(n.startswith('fc.') or (stage=='partial' and n.startswith('layer4.')) for n in changed)
        assert all(torch.equal(b,before[n]) for n,b in model.named_buffers())
        rows.append(dict(stage=stage,actual_pretrained=args.pretrained,trainable_params=sum(r['numel'] for r in report if r['trainable']),
                         groups=len(optimizer.param_groups),changed_parameters=len(changed),bn_buffers_unchanged=True))
        pd.DataFrame(report).to_csv(out/f'parameters_{stage}.csv',index=False)
    pd.DataFrame(rows).to_csv(out/'freeze_contract.csv',index=False)
    print(pd.DataFrame(rows).to_string(index=False))
    print('실제 사전학습 실행' if args.pretrained else 'STRUCTURE ONLY: weights=None. 전이 성능/정확도 결과가 아니다.')
if __name__=='__main__': main()
