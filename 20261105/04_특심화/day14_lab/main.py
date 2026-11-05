"""특심화 실행: python main.py --mode full|part|resume|audit|cam|bootstrap|stages"""
from pathlib import Path
import argparse,json,random,copy
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader,TensorDataset
from engine import datasets,evaluate,experiment
from models import build_model
from contracts import *


def run(mode,amp=False):
    torch.set_num_threads(1);torch.manual_seed(14);np.random.seed(14);random.seed(14)
    base=Path(__file__).resolve().parent;data=base/'data';out=base/'outputs';out.mkdir(exist_ok=True)
    if mode=='audit':
        result=audit_manifest(data);(out/'audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps({k:len(result[k]) for k in ['records','exact_groups','near_pairs','group_leaks']},sort_keys=True));return
    if mode in {'cam','bootstrap','stages'}:
        model,summary,history,prediction=experiment(data,epochs=1)  # 초기 후보 진단; 최종 성능 추정이 아닙니다.
        if mode=='bootstrap':
            manifest=pd.read_csv(data/'manifest.csv').set_index('path');groups=manifest.loc[prediction.path,'group_id'].to_numpy()
            result=group_bootstrap(prediction.actual,prediction.predicted,groups)
            (out/'bootstrap.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
            _,valid=datasets(data)
            brightness=np.array([valid[i][0].mean().item() for i in range(len(valid))])
            slices=[]
            for name,mask in [('brightness_lt_035',brightness<.35),('brightness_ge_035',brightness>=.35)]:
                if mask.sum()>=2 and len(np.unique(groups[mask]))>=2:
                    row=group_bootstrap(prediction.actual.to_numpy()[mask],prediction.predicted.to_numpy()[mask],groups[mask])
                    row.update({'slice':name,'n':int(mask.sum())});slices.append(row)
            pd.DataFrame(slices).to_csv(out/'slice_metrics.csv',index=False)
            print(json.dumps(result,sort_keys=True));print('사전 정의 밝기 slice 수:',len(slices));return
        if mode=='cam':
            import cv2
            _,valid=datasets(data);x,_=valid[0];x=x[None];target=int(prediction.loc[0,'predicted'])
            results=[]
            for name,layer in [('shallow',model[2]),('deep',model[6])]:
                cam=grad_cam(model,x,layer,target)
                cv2.imwrite(str(out/f'{name}_cam.png'),cv2.resize(cv2.applyColorMap(np.uint8(cam.numpy()*255),cv2.COLORMAP_JET),(256,256)))
                # 같은 입력의 상위 10% CAM 픽셀 가림과 같은 크기의 무작위 가림을 비교(인과 증명 아님).
                k=max(1,int(cam.numel()*.1));mask=torch.ones_like(x)
                take=cam.flatten().topk(k).indices
                mask.reshape(3,-1)[:,take]=0
                random_mask=torch.ones_like(x);g=torch.Generator().manual_seed(14);random_mask.reshape(3,-1)[:,torch.randperm(cam.numel(),generator=g)[:k]]=0
                with torch.no_grad():
                    base_score=model(x)[0,target].item();high=model(x*mask)[0,target].item();rnd=model(x*random_mask)[0,target].item()
                results.append({'layer':name,'target':target,'drop_top':base_score-high,'drop_random':base_score-rnd})
            score,drop=occlusion_map(model,x,target);np.save(out/'occlusion.npy',drop.numpy())
            pd.DataFrame(results).to_csv(out/'explanation_comparison.csv',index=False)
            print(pd.DataFrame(results).round(4).to_string(index=False));print('주의: 가림은 분포 밖 입력일 수 있음');return
        if mode=='stages':
            model=build_model(data);optimizer=torch.optim.AdamW(trainable_groups(model,'head'),weight_decay=.0001)
            train,_=datasets(data);x=torch.stack([train[i][0] for i in range(8)]);y=torch.tensor(train.targets[:8])
            model.eval();optimizer.zero_grad();nn.functional.cross_entropy(model(x),y).backward();optimizer.step()
            old={id(p):copy.deepcopy(optimizer.state[p]) for p in model[9].parameters()}
            # 제공된 선택 예: Head의 optimizer state를 유지하면서 새 층만 추가한다.
            new_params=list(model[4:6].parameters())
            for p in new_params:p.requires_grad_(True)
            optimizer.add_param_group({'params':new_params,'lr':.001})
            print('optimizer group 수:',len(optimizer.param_groups))
            print('Head step 보존:',all(torch.equal(old[id(p)]['step'],optimizer.state[p]['step']) for p in model[9].parameters()))
            return
    device=torch.device('cuda' if amp else 'cpu')
    if amp and not torch.cuda.is_available():raise RuntimeError('CUDA unavailable; CPU run: omit --amp')
    train,valid=datasets(data)
    x=torch.stack([train[i][0] for i in range(len(train))]);y=torch.tensor(train.targets)
    g=torch.Generator().manual_seed(14)
    loader=DataLoader(TensorDataset(x,y,torch.arange(len(y))),batch_size=16,shuffle=True,generator=g,num_workers=0)
    valid_x=torch.stack([valid[i][0] for i in range(len(valid))]);valid_y=torch.tensor(valid.targets)
    model=build_model(data).to(device);optimizer=torch.optim.AdamW(trainable_groups(model,'partial'),weight_decay=.0001)
    scheduler=torch.optim.lr_scheduler.StepLR(optimizer,step_size=2,gamma=.5)
    scaler=torch.amp.GradScaler('cuda',enabled=amp)
    weights,_=imbalance_weights(y)
    config={'seed':14,'epochs':4,'batch_size':16,'strategy':'partial','amp':amp,'bn':'frozen','source':'synthetic','classes':3}
    sig=signature(data);start=0;history=[]
    if mode=='resume':start,history=load_checkpoint(out/'part.pt',model,optimizer,scheduler,scaler,g,config,sig)
    stop=2 if mode=='part' else 4
    for epoch in range(start+1,stop+1):
        loss,order=train_epoch(model,loader,optimizer,weights,scaler,amp=amp)
        model.eval()
        with torch.no_grad():vl=nn.functional.cross_entropy(model(valid_x.to(device)),valid_y.to(device)).item()
        scheduler.step();history.append({'epoch':epoch,'train_objective':loss,'valid_loss':vl,'lr':[group['lr'] for group in optimizer.param_groups],'order':order})
    save_checkpoint(out/f'{mode}.pt',model,optimizer,scheduler,scaler,g,stop,history,config,sig)
    (out/f'{mode}.json').write_text(json.dumps(history,indent=2),encoding='utf-8')
    print(json.dumps({'mode':mode,'epoch':stop,'train_objective':round(history[-1]['train_objective'],6),'valid_loss':round(history[-1]['valid_loss'],6),'test_used':False},sort_keys=True))


def main():
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['full','part','resume','audit','cam','bootstrap','stages'],default='full');p.add_argument('--amp',action='store_true');a=p.parse_args();run(a.mode,a.amp)

if __name__=='__main__':main()
