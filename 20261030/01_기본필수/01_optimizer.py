from pathlib import Path
import pandas as pd
import torch
from torch import nn

torch.set_num_threads(1)
base = Path(__file__).resolve().parent
df = pd.read_csv(base / "points.csv")
train = df[df["split"] == "train"]
valid = df[df["split"] == "valid"]
X_train = torch.tensor(train[["x1", "x2"]].values, dtype=torch.float32)
y_train = torch.tensor(train["label"].values, dtype=torch.long)
X_valid = torch.tensor(valid[["x1", "x2"]].values, dtype=torch.float32)
y_valid = torch.tensor(valid["label"].values, dtype=torch.long)
# test 4건은 읽은 표에만 있으며 학습/평가 Tensor로 만들지 않습니다.

loss_fn = nn.CrossEntropyLoss()
for name in ["SGD", "AdamW"]:
    # 후보마다 같은 초기 가중치에서 다시 시작합니다. 앞 모델을 이어 학습하지 않습니다.
    torch.manual_seed(42)
    model = nn.Sequential(nn.Linear(2, 8), nn.ReLU(), nn.Linear(8, 2))
    if name == "SGD":
        # SGD의 학습할 파라미터는 model.parameters()입니다. lr=0.01, momentum=0.0으로 만드세요.
        # 학습률은 기본값에 기대지 않고 명시하며, 두 Optimizer 모두 weight_decay=0.0으로 비교합니다.
        # >>> B01
        # TODO B01: 위 요구사항에 맞게 이 블록만 완성합니다.
        optimizer = torch.optim.SGD(model.parameters(), lr=0.0)
        # <<< B01
    else:
        # AdamW를 같은 lr=0.01로 만드세요. weight_decay=0.0을 반드시 적으세요.
        # 이번에는 감쇠 효과가 아닌 갱신 규칙을 비교합니다. 이 공통 lr이 두 알고리즘의 최적 lr이라는 뜻은 아닙니다.
        # >>> B02
        # TODO B02: 위 요구사항에 맞게 이 블록만 완성합니다.
        optimizer = torch.optim.AdamW(model.parameters(), lr=0.0, weight_decay=0.0)
        # <<< B02
    for epoch in range(20):
        model.train()
        optimizer.zero_grad()
        loss = loss_fn(model(X_train), y_train)
        loss.backward()
        optimizer.step()
    model.eval()
    with torch.no_grad():
        valid_loss = loss_fn(model(X_valid), y_valid).item()
    print(name, "20 epochs / valid loss:", round(valid_loss, 6))
