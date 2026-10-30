from pathlib import Path
import json
import torch
import pandas as pd
BASE=Path(__file__).resolve().parent
OUT=BASE/'outputs';OUT.mkdir(exist_ok=True)
torch.set_num_threads(1)

import copy
from torch.utils.data import TensorDataset,DataLoader
from support import load_data,build_model
from tasks import EarlyStop,evaluate_batches,restore_best
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
X,y,Xv,yv,ids,_=load_data();X,y=X[:60],y[:60]
torch.manual_seed(42)
model=build_model(dict(width=64,dropout=.1))
optimizer=torch.optim.AdamW(model.parameters(),lr=.01,weight_decay=0.)
scheduler=torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer,mode='min',factor=.5,patience=3,threshold=.001,threshold_mode='abs')
loader=DataLoader(TensorDataset(X,y),batch_size=16,shuffle=True,generator=torch.Generator().manual_seed(43))
stopper=EarlyStop(patience=8,min_delta=.001);history=[]
for epoch in range(1,61):
    model.train();used=optimizer.param_groups[0]['lr'];total=0.;seen=0
    for xb,yb in loader:
        optimizer.zero_grad(set_to_none=True)
        loss=torch.nn.functional.cross_entropy(model(xb),yb);loss.backward();optimizer.step()
        total+=loss.item()*len(yb);seen+=len(yb)
    train=evaluate_batches(model,[(X,y)])
    valid=evaluate_batches(model,list(zip(Xv.split(32),yv.split(32))))
    scheduler.step(valid['loss']);stop=stopper.update(valid['loss'],epoch,model)
    history.append(dict(epoch=epoch,train_loss_step=total/seen,train_loss_eval=train['loss'],valid_loss=valid['loss'],
        valid_acc=valid['accuracy'],lr_used=used,lr_next=optimizer.param_groups[0]['lr'],bad_epochs=stopper.bad))
    if stop: break
last_valid=history[-1]['valid_loss'];selected=restore_best(model,stopper)
restored=evaluate_batches(model,[(Xv,yv)])
report={**selected,'stop_epoch':epoch,'last_valid_loss':last_valid,'restored_valid_loss':restored['loss'],
    'restored_matches_best':abs(restored['loss']-selected['best_loss'])<1e-6,'test_used':False}
table=pd.DataFrame(history);table.to_csv(OUT/'history.csv',index=False)
torch.save(model.state_dict(),OUT/'best_model.pt')
(OUT/'stopping_report.json').write_text(json.dumps(report,indent=2),encoding='utf8')
plt.figure(figsize=(8,5));plt.plot(table.epoch,table.train_loss_eval,label='Train: evaluation mode')
plt.plot(table.epoch,table.valid_loss,label='Validation');plt.axvline(selected['best_epoch'],linestyle='--',label='Observed best')
plt.xlabel('Epoch');plt.ylabel('Cross-entropy');plt.legend();plt.tight_layout();plt.savefig(OUT/'learning_curve.png',dpi=150);plt.close()
print(json.dumps(report,indent=2))
