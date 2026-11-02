import torch
from torch import nn
torch.set_num_threads(1)  # 작은 CPU 실습의 실행 조건을 고정한다.
torch.manual_seed(42)
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"outputs"
OUT.mkdir(exist_ok=True)
df=pd.read_csv(ROOT/"data"/"series.csv")
train=torch.tensor(df.loc[df["split"]=="train","value"].values,dtype=torch.float32)
valid=torch.tensor(df.loc[df["split"]=="valid","value"].values,dtype=torch.float32)

from copy import deepcopy
w=train.unfold(0,13,1); v=valid.unfold(0,13,1)
x,y=w[:,:12].unsqueeze(-1),w[:,12:13]
vx,vy=v[:,:12].unsqueeze(-1),v[:,12:13]
rows=[]
for name in ["RNN","LSTM"]:
    torch.manual_seed(42)
    core=nn.RNN(1,8,batch_first=True) if name=="RNN" else nn.LSTM(1,8,batch_first=True)
    head=nn.Linear(8,1); params=list(core.parameters())+list(head.parameters())
    optimizer=torch.optim.Adam(params,lr=0.02); best=float("inf")
    for epoch in range(1,41):
        core.train(); head.train(); optimizer.zero_grad(); output,_=core(x)
        # TODO A03: 각 과거 Window의 마지막 출력에서 다음 값에 대한 MSE를 계산한다.
        # BEGIN A03
        loss=nn.MSELoss()(head(output[:,0]),y)
        # END A03
        loss.backward(); optimizer.step(); core.eval(); head.eval()
        with torch.inference_mode():
            output,_=core(vx); score=nn.MSELoss()(head(output[:,-1]),vy).item()
        if score<best: best=score; best_epoch=epoch
    rows.append({"model":name,"hidden":8,"params":sum(p.numel() for p in params),
                 "epochs":40,"best_epoch":best_epoch,"valid_mse":best})
# 마지막 관측을 다음 값으로 쓰는 학습 없는 기준선도 기록한다.
rows.append({"model":"Persistence","hidden":0,"params":0,"epochs":0,"best_epoch":0,
             "valid_mse":nn.MSELoss()(vx[:,-1],vy).item()})
table=pd.DataFrame(rows); table.to_csv(OUT/"forecast_comparison.csv",index=False)
print("windows:",len(x),len(vx),"test 미사용")
print(table.round(6).to_string(index=False))
