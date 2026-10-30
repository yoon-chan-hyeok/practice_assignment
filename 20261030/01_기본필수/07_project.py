from pathlib import Path
import pandas as pd
import torch
from torch import nn

torch.set_num_threads(1)
base = Path(__file__).resolve().parent
import matplotlib
matplotlib.use("Agg")  # 창을 띄우지 않고 PNG에 저장합니다.
import matplotlib.pyplot as plt
df = pd.read_csv(base / "points.csv")
train = df[df["split"] == "train"]
valid = df[df["split"] == "valid"]
X_train = torch.tensor(train[["x1", "x2"]].values, dtype=torch.float32)
y_train = torch.tensor(train["label"].values, dtype=torch.long)
X_valid = torch.tensor(valid[["x1", "x2"]].values, dtype=torch.float32)
y_valid = torch.tensor(valid["label"].values, dtype=torch.long)
# test 4건은 읽은 표에만 있으며 학습/평가 Tensor로 만들지 않습니다.

# 실습 07~08: 기준 lr과 비교 lr만 다릅니다. 더 나쁘게 나와도 그대로 보고합니다.
loss_fn = nn.CrossEntropyLoss()
summary = []
for name, lr in [("baseline", 0.001), ("candidate", 0.01)]:
    torch.manual_seed(42)
    model = nn.Sequential(nn.Linear(2, 8), nn.ReLU(), nn.Linear(8, 2))
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.0)
    history = []
    for epoch in range(1, 21):
        model.train()
        optimizer.zero_grad()
        loss = loss_fn(model(X_train), y_train)
        # 이미 zero_grad와 loss 계산이 끝났습니다. loss.backward() 다음 optimizer.step()을 호출하세요.
        # 학습 데이터만 사용합니다. 비교 후보마다 모델을 처음부터 새로 만듭니다.
        # >>> B08
        # TODO B08: 위 요구사항에 맞게 이 블록만 완성합니다.
        pass
        # <<< B08
        model.eval()
        with torch.no_grad():
            train_loss = loss_fn(model(X_train), y_train).item()
            valid_loss = loss_fn(model(X_valid), y_valid).item()
        # 한 epoch의 번호와 갱신 후 train_loss, valid_loss를 기록하세요.
        # history.append([epoch, train_loss, valid_loss]) 형태로 추가합니다.
        # >>> B09
        # TODO B09: 위 요구사항에 맞게 이 블록만 완성합니다.
        history.append([epoch, train_loss, 0.0])
        # <<< B09
    table = pd.DataFrame(history, columns=["epoch", "train_loss_eval", "valid_loss"])
    table.to_csv(base / f"history_{name}.csv", index=False)
    best = table.loc[table["valid_loss"].idxmin()]
    summary.append([name, lr, int(best["epoch"]), best["valid_loss"]])
    plt.figure(figsize=(8, 5))
    plt.plot(table["epoch"], table["train_loss_eval"], label="train (eval mode)")
    plt.plot(table["epoch"], table["valid_loss"], label="valid")
    plt.axvline(best["epoch"], linestyle="--", label="best epoch")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.tight_layout()
    plt.savefig(base / f"curves_{name}.png", dpi=150)
    plt.close()
result = pd.DataFrame(summary, columns=["setting", "lr", "best_epoch", "best_valid_loss"])
result.to_csv(base / "experiment_table.csv", index=False)
print(result.round(6).to_string(index=False))
print("test 미사용 / best epoch는 관찰한 최소 지점, 기본필수에서는 모델 저장·복원하지 않음")
