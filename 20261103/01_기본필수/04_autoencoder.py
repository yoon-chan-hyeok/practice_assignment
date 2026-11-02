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

x = train.unfold(0,8,1).contiguous()
v = valid.unfold(0,8,1).contiguous()
model = nn.Sequential(nn.Linear(8,2),nn.Tanh(),nn.Linear(2,8))
optimizer = torch.optim.Adam(model.parameters(),lr=0.03)
for epoch in range(40):
    optimizer.zero_grad()
    reconstructed = model(x)
    # TODO B04: Autoencoder의 정답을 입력 x 자체로 설정한다.
    # 정상 데이터를 0으로 바꾸는 과제가 아니다. reconstruction과 x를 비교한다.
    # BEGIN B04
    loss = nn.MSELoss()(reconstructed, torch.zeros_like(x))
    # END B04
    loss.backward()
    optimizer.step()
model.eval()
with torch.inference_mode():
    latent = model[:2](v)
    error = nn.MSELoss()(model(v),v).item()
print("train:", tuple(x.shape), "valid:", tuple(v.shape))
print("latent / 복원:", tuple(latent.shape), tuple(model(v).shape))
print("valid MSE:", round(error,6))
