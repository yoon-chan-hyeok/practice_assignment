"""제공 학습 실행부: checkpoint 기능과 상태 비교만 tasks.py에서 구현합니다."""
import random
from pathlib import Path
import pandas as pd
import torch
from torch.utils.data import TensorDataset,DataLoader
from support import load_data,build_model
from stopping import EarlyStop,evaluate_batches
from tasks import save_checkpoint,restore_checkpoint

BASE=Path(__file__).resolve().parent
CONFIG=dict(seed=42,width=16,norm='batch',dropout=.25,lr=.01,weight_decay=.01,
            epochs=20,batch_size=32,stop_patience=100,min_delta=.001)

def execute(part):
    torch.set_num_threads(1);torch.use_deterministic_algorithms(True)
    random.seed(CONFIG['seed']);torch.manual_seed(CONFIG['seed'])
    X,y,Xv,yv,ids,fingerprint=load_data()
    model=build_model(CONFIG)
    optimizer=torch.optim.AdamW(model.parameters(),lr=CONFIG['lr'],weight_decay=CONFIG['weight_decay'])
    scheduler=torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer,mode='min',factor=.5,patience=2,threshold=.02,threshold_mode='abs')
    stopper=EarlyStop(CONFIG['stop_patience'],CONFIG['min_delta'])
    generator=torch.Generator().manual_seed(CONFIG['seed']+1)
    loader=DataLoader(TensorDataset(X,y,torch.arange(len(y))),batch_size=CONFIG['batch_size'],shuffle=True,
                      generator=generator,num_workers=0)
    metadata=dict(config=CONFIG.copy(),fingerprint=fingerprint,split_ids=ids,device='cpu',
                  environment={'torch':str(torch.__version__),'threads':1},completed_epochs=0)
    start=0;history=[];traces=[];out=BASE/'outputs';out.mkdir(exist_ok=True)
    if part=='resume':
        start,history,traces=restore_checkpoint(out/'cut.pt',model,optimizer,scheduler,stopper,generator,metadata)
    limit=10 if part=='first' else 20
    for epoch in range(start+1,limit+1):
        model.train();total=0.;seen=0;trace=[];used=optimizer.param_groups[0]['lr']
        for xb,yb,index in loader:
            optimizer.zero_grad(set_to_none=True)
            loss=torch.nn.functional.cross_entropy(model(xb),yb);loss.backward();optimizer.step()
            total+=loss.item()*len(yb);seen+=len(yb);trace.extend(index.tolist())
        tr=evaluate_batches(model,[(X,y)]);va=evaluate_batches(model,[(Xv,yv)])
        scheduler.step(va['loss']);stopper.update(va['loss'],epoch,model)
        history.append(dict(epoch=epoch,train_loss_step=total/seen,train_loss_eval=tr['loss'],valid_loss=va['loss'],
                            valid_acc=va['accuracy'],lr_used=used,lr_next=optimizer.param_groups[0]['lr']))
        traces.append(trace)
    metadata['completed_epochs']=limit
    name={'full':'full.pt','first':'cut.pt','resume':'resumed.pt'}[part]
    save_checkpoint(out/name,model,optimizer,scheduler,stopper,generator,metadata,history,traces)
    pd.DataFrame(history).to_csv(out/(part+'_history.csv'),index=False)
