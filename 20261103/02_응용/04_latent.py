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

x=train.unfold(0,8,1).contiguous(); v=valid.unfold(0,8,1).contiguous(); rows=[]
for latent_size in [1,2,4]:
    torch.manual_seed(42)
    # TODO A04: 후보 latent_size=1·2·4를 실제 Encoder·Decoder 크기에 적용한다.
    # BEGIN A04
    model=nn.Sequential(nn.Linear(8,2),nn.Tanh(),nn.Linear(2,8))
    # END A04
    optimizer=torch.optim.Adam(model.parameters(),lr=0.02); best=float("inf")
    for epoch in range(1,41):
        optimizer.zero_grad(); loss=nn.MSELoss()(model(x),x); loss.backward(); optimizer.step()
        with torch.inference_mode(): score=nn.MSELoss()(model(v),v).item()
        if score<best: best=score; best_epoch=epoch
    rows.append({"latent":latent_size,"retained_ratio":latent_size/8,
                 "params":sum(p.numel() for p in model.parameters()),"best_epoch":best_epoch,"valid_mse":best})
table=pd.DataFrame(rows); table.to_csv(OUT/"latent_comparison.csv",index=False)
print(table.round(6).to_string(index=False))
