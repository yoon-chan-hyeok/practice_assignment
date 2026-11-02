from pathlib import Path
import copy
import csv
import json
import time
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import pandas as pd

torch.manual_seed(42)
torch.set_num_threads(1)
root = Path(__file__).resolve().parent
out = root / "outputs"
out.mkdir(exist_ok=True)

transform = transforms.Compose([transforms.Resize((32, 32)), transforms.ToTensor()])
train = datasets.ImageFolder(root / "data" / "train", transform=transform)
valid = datasets.ImageFolder(root / "data" / "valid", transform=transform)
train_loader = DataLoader(train, batch_size=16, shuffle=True, num_workers=0,
                          generator=torch.Generator().manual_seed(42))
valid_loader = DataLoader(valid, batch_size=16, shuffle=False, num_workers=0)

model = nn.Sequential(
    nn.Conv2d(3, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Linear(32, 2),
)

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=0.01, weight_decay=0.0)
history = []
best_loss = float("inf")
for epoch in range(1, 6):
    model.train()
    for images, labels in train_loader:
        optimizer.zero_grad()
        loss = loss_fn(model(images), labels)
        # BEGIN A05
        # TODO A05: loss 역전파와 가중치 갱신을 순서대로 실행한다.
        pass
        # END A05
    # 같은 epoch 말 모델을 eval 모드로 평가해 train/valid의 측정 조건을 맞춘다.
    model.eval()
    row = {"epoch": epoch}
    with torch.no_grad():
        for phase, loader in [("train", DataLoader(train, batch_size=16)), ("valid", valid_loader)]:
            total_loss, correct, count = 0.0, 0, 0
            for images, labels in loader:
                logits = model(images)
                total_loss += loss_fn(logits, labels).item() * len(labels)
                correct += (logits.argmax(1) == labels).sum().item()
                count += len(labels)
            row[phase+"_loss"] = total_loss/count
            row[phase+"_accuracy"] = correct/count
    history.append(row)
    if row["valid_loss"] < best_loss:
        best_loss, best_epoch = row["valid_loss"], epoch
        best_state = copy.deepcopy(model.state_dict())
model.load_state_dict(best_state)
model.eval()
actual, predicted = [], []
with torch.no_grad():
    for images, labels in valid_loader:
        actual.extend(labels.tolist())
        predicted.extend(model(images).argmax(1).tolist())
cm = torch.zeros(2, 2, dtype=torch.long)
for truth, guess in zip(actual, predicted):
    cm[truth, guess] += 1
print(pd.DataFrame(history).round(4).to_string(index=False))
print("best epoch:", best_epoch)
print("혼동행렬 행=실제, 열=예측:\n", cm.tolist())
print("클래스별 정답 수:", cm.diag().tolist(), "/", cm.sum(1).tolist())
pd.DataFrame(history).to_csv(out / "cnn_history.csv", index=False)
pd.DataFrame(cm.numpy(), index=train.classes, columns=train.classes).to_csv(out / "confusion_matrix.csv")
pd.DataFrame(dict(file=[Path(p).name for p,_ in valid.samples], actual=actual, predicted=predicted)).to_csv(out / "cnn_predictions.csv", index=False)
