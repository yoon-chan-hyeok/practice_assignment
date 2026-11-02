"""실습 08 · small은 오프라인 가능. head/partial은 실제 공식 가중치가 필요하다."""
from pathlib import Path
import argparse
import copy
import json
import time
import shutil
import torch
from torch import nn
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from data import load_data
from models import build_model
from train import train_epoch, evaluate

ROOT = Path(__file__).resolve().parent

def run(kind, width=16, augment=False, epochs=5, out=None):
    torch.manual_seed(42)
    torch.set_num_threads(1)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    out = Path(out) if out else ROOT / "outputs"
    out.mkdir(parents=True, exist_ok=True)
    batch = 16 if kind=="small" else 4
    train, train_eval, valid, loader, train_check, valid_loader = load_data(kind, augment, batch)
    model = build_model(kind, width=width).to(device)
    if kind=="partial":
        params=[{"params": model.fc.parameters(), "lr":0.001}, {"params":model.layer4.parameters(), "lr":0.0001}]
    elif kind=="head":
        params=model.fc.parameters()
    else:
        params=model.parameters()
    optimizer=torch.optim.AdamW(params,lr=0.01 if kind=="small" else 0.001,weight_decay=0.0001)
    history=[]
    best_loss=float("inf")
    if device.type=="cuda": torch.cuda.synchronize(device)
    start=time.perf_counter()
    for epoch in range(1,epochs+1):
        train_epoch(model,loader,optimizer,device,kind)
        train_loss,train_acc,_,_=evaluate(model,train_check,device)
        valid_loss,valid_acc,_,_=evaluate(model,valid_loader,device)
        history.append(dict(epoch=epoch,train_loss=train_loss,valid_loss=valid_loss,train_accuracy=train_acc,valid_accuracy=valid_acc))
        # BEGIN D09
        # TODO D09: valid loss가 작아질 때 best 상태를 복사해서 기록한다.
        if valid_loss < best_loss:
            best_loss, best_epoch = valid_loss, epoch
            best_state = model.state_dict()
        # END D09
    if device.type=="cuda": torch.cuda.synchronize(device)
    seconds=time.perf_counter()-start
    model.load_state_dict(best_state)
    loss,accuracy,logits,labels=evaluate(model,valid_loader,device)
    pred=logits.argmax(1)
    cm=torch.zeros(2,2,dtype=torch.int64)
    for a,b in zip(labels,pred): cm[a,b]+=1
    name=kind if width==16 and not augment else f"{kind}_w{width}_aug{int(augment)}"
    table=pd.DataFrame(history);table["is_best"]=table.epoch==best_epoch
    table.to_csv(out/f"history_{name}.csv",index=False)
    files=[Path(p).relative_to(ROOT/'data').as_posix() for p,_ in valid.samples]
    predictions=pd.DataFrame(dict(file=files,actual=labels.tolist(),predicted=pred.tolist(),
                                  probability_vertical=logits.softmax(1)[:,1].tolist()))
    predictions.to_csv(out/f"predictions_{name}.csv",index=False)
    pd.DataFrame(cm.numpy(),index=train.classes,columns=train.classes).to_csv(out/f"confusion_{name}.csv")
    error_dir=out/f"errors_{name}"
    if error_dir.exists(): shutil.rmtree(error_dir)
    error_dir.mkdir()
    for i in range(len(valid)):
        if labels[i]!=pred[i]:
            path=Path(valid.samples[i][0])
            shutil.copy2(path,error_dir/f"actual{int(labels[i])}_pred{int(pred[i])}_{path.name}")
    (error_dir/'README.txt').write_text(f"오분류 {int((labels!=pred).sum())}건. 0건이어도 실제 서비스 성능 보장은 아니다.\n",encoding='utf-8')
    normalize=None if kind=="small" else {"mean":[0.485,0.456,0.406],"std":[0.229,0.224,0.225]}
    checkpoint=dict(state_dict={k:v.detach().cpu() for k,v in best_state.items()},kind=kind,width=width,
                    classes=train.classes,class_to_idx=train.class_to_idx,image_size=32 if kind=="small" else 224,
                    normalize=normalize,best_epoch=best_epoch,seed=42,
                    source_weights="none" if kind=="small" else "IMAGENET1K_V1",torch_version=str(torch.__version__))
    torch.save(checkpoint,out/f"best_{name}.pt")
    plt.figure(figsize=(7,4))
    plt.plot(table.epoch,table.train_loss,label='train (eval)')
    plt.plot(table.epoch,table.valid_loss,label='valid')
    plt.xlabel('Epoch');plt.ylabel('Cross entropy');plt.legend();plt.tight_layout()
    plt.savefig(out/f"curve_{name}.png",dpi=130);plt.close()
    row=dict(model=name,trainable_params=sum(p.numel() for p in model.parameters() if p.requires_grad),
             best_epoch=best_epoch,valid_loss=loss,valid_accuracy=accuracy,epochs=epochs,
             image_size=checkpoint['image_size'],augment=augment,device=str(device),training_seconds=seconds)
    print(name,"best",best_epoch,"valid loss",round(loss,4),"accuracy",round(accuracy,4))
    return row

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('--models',nargs='+',choices=['small','head','partial'],default=['small'])
    parser.add_argument('--epochs',type=int,default=3)
    args=parser.parse_args()
    rows=[run(kind,epochs=args.epochs) for kind in args.models]
    pd.DataFrame(rows).to_csv(ROOT/'outputs'/'model_comparison.csv',index=False)
