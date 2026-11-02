"""제공된 학습 실행기. 08의 과제는 체크포인트 pack/restore/대조다."""
from pathlib import Path
import argparse
import torch
from torch import nn
from torch.utils.data import DataLoader
from support import seed_all,small_model,image_dataset,fingerprint,save_json
from tasks import pack_state,restore_state

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--epochs',type=int,default=4)
    parser.add_argument('--stop-after',type=int);parser.add_argument('--resume');parser.add_argument('--out',required=True)
    args=parser.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    seed_all();config=dict(model='CNN4_8',batchnorm=True,dropout=0.2,classes=['horizontal','vertical'],
        resize=32,train_augment='horizontal_flip',batch_size=16,workers=0,seed=42,planned_epochs=args.epochs,device='cpu')
    ds=image_dataset('train',augment=True,with_index=True)
    generator=torch.Generator().manual_seed(42)
    loader=DataLoader(ds,batch_size=16,shuffle=True,generator=generator,num_workers=0)
    model=small_model(batchnorm=True,dropout=0.2)
    optimizer=torch.optim.AdamW(model.parameters(),lr=0.005,weight_decay=0.0001)
    scheduler=torch.optim.lr_scheduler.StepLR(optimizer,step_size=2,gamma=0.5)
    scaler=torch.amp.GradScaler('cuda',enabled=False)
    data_hash=fingerprint();start=0;history=[]
    if args.resume:
        saved=torch.load(args.resume,map_location='cpu',weights_only=True)
        start,history=restore_state(saved,model,optimizer,scheduler,scaler,generator,config,data_hash)
    end=min(args.epochs,args.stop_after) if args.stop_after else args.epochs
    if not 0<=start<=end: raise ValueError('epoch 범위 오류')
    for epoch in range(start,end):
        model.train();total=0.;seen=0;order=[]
        for x,y,ids in loader:
            optimizer.zero_grad(set_to_none=True)
            loss=nn.functional.cross_entropy(model(x),y)
            loss.backward();optimizer.step()
            total+=loss.item()*len(y);seen+=len(y);order.extend(ids.tolist())
        scheduler.step()
        history.append(dict(epoch=epoch+1,loss=total/seen,order=order,lr_next=optimizer.param_groups[0]['lr']))
    saved=pack_state(model,optimizer,scheduler,scaler,generator,end,history,config,data_hash)
    torch.save(saved,out/'checkpoint.pt');save_json('history.json',history,out)
    print('마친 epoch:',end,'train 이미지/epoch:',len(ds),'test 미사용')
if __name__=='__main__': main()
