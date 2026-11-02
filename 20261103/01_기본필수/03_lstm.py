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

# unfold(0,13,1): 과거 12개+다음 정답 1개인 묶음을 만든다.
window = train.unfold(0,13,1)
x = window[:,:12].unsqueeze(-1)
y = window[:,12:13]
lstm = nn.LSTM(1,8,batch_first=True)
head = nn.Linear(8,1)
output, (h_n,c_n) = lstm(x)
# TODO B03: 12개 관측의 마지막 은닉 출력으로 다음 값 1개를 예측한다.
# [:, -1, :]는 마지막 시점이다. 이 예제의 Window 길이는 모두 12이다.
# BEGIN B03
prediction = head(output[:, 0, :])
# END B03
print("입력 / 정답:", tuple(x.shape), tuple(y.shape))
print("h_n / c_n:", tuple(h_n.shape), tuple(c_n.shape))
print("예측:", tuple(prediction.shape))
print("첫 예측:", round(prediction[0].item(),6))
print("학습 전 MSE:", round(nn.MSELoss()(prediction,y).item(),6))
