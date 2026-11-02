import torch
from torch import nn
torch.set_num_threads(1)  # 작은 CPU 실습의 실행 조건을 고정한다.
torch.manual_seed(42)
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parent
df = pd.read_csv(ROOT / "series.csv")
# 시간 구간을 먼저 분리한다. test 구간은 모델에 넣지 않는다.
train = torch.tensor(df.loc[df["split"]=="train","value"].values,dtype=torch.float32)
valid = torch.tensor(df.loc[df["split"]=="valid","value"].values,dtype=torch.float32)

from copy import deepcopy
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
w = train.unfold(0,13,1); vw = valid.unfold(0,13,1)
x,y = w[:,:12].unsqueeze(-1), w[:,12:13]
vx,vy = vw[:,:12].unsqueeze(-1), vw[:,12:13]
core = nn.LSTM(1,8,batch_first=True); head = nn.Linear(8,1)
optimizer = torch.optim.Adam(list(core.parameters())+list(head.parameters()),lr=0.03)
rows=[]; best=float("inf")
for epoch in range(1,41):
    core.train(); head.train(); optimizer.zero_grad()
    output,_ = core(x)
    # TODO B08: LSTM의 마지막 관측 상태에서 다음 값을 계산한다.
    # BEGIN B08
    prediction = head(output[:, 0])
    # END B08
    loss=nn.MSELoss()(prediction,y); loss.backward(); optimizer.step()
    core.eval(); head.eval()
    with torch.inference_mode():
        out,_=core(vx); vp=head(out[:,-1]); vl=nn.MSELoss()(vp,vy).item()
        out,_=core(x); tl=nn.MSELoss()(head(out[:,-1]),y).item()
    rows.append({"task":"forecast","epoch":epoch,"train_mse":tl,"valid_mse":vl})
    if vl<best:
        best=vl; fepoch=epoch
        best_core=deepcopy(core.state_dict()); best_head=deepcopy(head.state_dict())
core.load_state_dict(best_core); head.load_state_dict(best_head)
with torch.inference_mode():
    out,_=core(vx); forecast=head(out[:,-1]).flatten()
# 별도 문제: 다음 값 예측이 아니라 8개 입력 자체를 복원한다.
ax=train.unfold(0,8,1).contiguous(); av=valid.unfold(0,8,1).contiguous()
torch.manual_seed(42)
ae=nn.Sequential(nn.Linear(8,2),nn.Tanh(),nn.Linear(2,8))
optimizer=torch.optim.Adam(ae.parameters(),lr=0.03); best=float("inf")
for epoch in range(1,41):
    ae.train(); optimizer.zero_grad(); reconstructed=ae(ax)
    # TODO B09: 재구성의 target을 과거 8개 값인 ax로 지정한다.
    # BEGIN B09
    loss = nn.MSELoss()(reconstructed, torch.zeros_like(ax))
    # END B09
    loss.backward(); optimizer.step(); ae.eval()
    with torch.inference_mode():
        tl=nn.MSELoss()(ae(ax),ax).item(); vl=nn.MSELoss()(ae(av),av).item()
    rows.append({"task":"reconstruction","epoch":epoch,"train_mse":tl,"valid_mse":vl})
    if vl<best: best=vl; aepoch=epoch; best_ae=deepcopy(ae.state_dict())
ae.load_state_dict(best_ae)
with torch.inference_mode():
    restored=ae(av); errors=((restored-av)**2).mean(dim=1)
# valid의 실제 time ID와 함께 저장한다. test는 Window도 만들지 않는다.
valid_ids=df.loc[df["split"]=="valid","time"].tolist()
pd.DataFrame(rows).to_csv(ROOT/"history.csv",index=False)
pd.DataFrame({"time":valid_ids[12:],"actual":vy.flatten().tolist(),"prediction":forecast.tolist()}).to_csv(ROOT/"predictions.csv",index=False)
pd.DataFrame({"end_time":valid_ids[7:],"mse":errors.tolist()}).to_csv(ROOT/"reconstruction.csv",index=False)
pd.DataFrame([{"task":"forecast","best_epoch":fepoch,"valid_mse":((forecast-vy.flatten())**2).mean().item()},
              {"task":"reconstruction","best_epoch":aepoch,"valid_mse":errors.mean().item()}]).to_csv(ROOT/"comparison.csv",index=False)
torch.save({"forecast_core":best_core,"forecast_head":best_head,"ae":best_ae,
            "lookback":12,"ae_features":8,"hidden_size":8,"split":"strict_time_segments"},ROOT/"best_model.pt")
plt.figure(figsize=(7,4)); plt.plot(av[0].tolist(),marker="o",label="Input")
plt.plot(restored[0].tolist(),marker="s",label="Reconstruction")
plt.xlabel("Position in window"); plt.ylabel("Signal"); plt.legend(); plt.tight_layout()
plt.savefig(ROOT/"mask_or_latent.png",dpi=120); plt.close()
print("forecast windows:",len(x),len(vx),"best epoch:",fepoch)
print("AE windows:",len(ax),len(av),"best epoch:",aepoch)
print(pd.read_csv(ROOT/"comparison.csv").round(6).to_string(index=False))
print("저장: history.csv / predictions.csv / reconstruction.csv / comparison.csv / best_model.pt / mask_or_latent.png")
print("test 구간: 보관 / 평가하지 않음")
