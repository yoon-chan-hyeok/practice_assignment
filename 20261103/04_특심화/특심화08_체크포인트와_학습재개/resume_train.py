"""제공 학습 실행기. tasks의 epoch·저장·복원 함수를 호출한다."""
from pathlib import Path
import argparse,json,hashlib,random
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader,TensorDataset
from models import RecurrentModel
from data import classification_data
from tasks import train_epoch,save_checkpoint,load_checkpoint
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--epochs',type=int,default=4)
    parser.add_argument('--output',default='outputs/full')
    parser.add_argument('--resume',default=None)
    args=parser.parse_args(); root=Path(__file__).resolve().parent
    if not 1<=args.epochs<=20: raise ValueError('epochs must be 1..20')
    torch.set_num_threads(1); torch.manual_seed(42); random.seed(42); np.random.seed(42)
    config={'seed':42,'batch_size':7,'hidden':8,'dropout':0.2,'lr':0.01,'scheduler':'StepLR(2,0.7)','num_workers':0,'device':'cpu'}
    data=classification_data(root/'data'); tr=data['train']; va=data['valid']
    model=RecurrentModel('LSTM',3,8,2); model.head=nn.Sequential(nn.Dropout(.2),nn.Linear(8,2))
    optimizer=torch.optim.Adam(model.parameters(),lr=.01); scheduler=torch.optim.lr_scheduler.StepLR(optimizer,step_size=2,gamma=.7)
    generator=torch.Generator().manual_seed(123)
    loader=DataLoader(TensorDataset(tr['x'],tr['lengths'],tr['y'],torch.arange(len(tr['y']))),batch_size=7,shuffle=True,generator=generator,num_workers=0)
    sha=hashlib.sha256((root/'data'/'sequences.json').read_bytes()).hexdigest()
    last=0; history=[]
    if args.resume:
        path=Path(args.resume); path=path if path.is_absolute() else root/path
        last,history=load_checkpoint(path,model,optimizer,scheduler,generator,config,sha)
    if args.epochs<last: raise ValueError('target epochs precede checkpoint')
    for epoch in range(last+1,args.epochs+1):
        loss,order=train_epoch(model,loader,optimizer)
        model.eval()
        with torch.inference_mode(): vl=nn.CrossEntropyLoss()(model(va['x'],va['lengths']),va['y']).item()
        scheduler.step()
        history.append({'epoch':epoch,'train_online_loss':loss,'valid_loss':vl,'next_lr':optimizer.param_groups[0]['lr'],'order':order})
    output=Path(args.output); output=output if output.is_absolute() else root/output; output.mkdir(parents=True,exist_ok=True)
    save_checkpoint(output/'checkpoint.pt',model,optimizer,scheduler,generator,args.epochs,history,config,sha)
    (output/'history.json').write_text(json.dumps(history,indent=2),encoding='utf-8')
    print('완료 epoch:',args.epochs,'history:',len(history),'valid loss:',round(history[-1]['valid_loss'],6))
    print('CPU / train60·valid20 / test 미사용 / epoch 경계 재개')

if __name__=='__main__': main()
