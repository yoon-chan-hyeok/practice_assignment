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
        # BEGIN A08
        # TODO A08: 이전 실습의 학습 갱신을 연결해 프로젝트를 실행한다.
        pass
        # END A08
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
actual, predicted, confidences = [], [], []
with torch.no_grad():
    for images, labels in valid_loader:
        actual.extend(labels.tolist())
        probabilities = model(images).softmax(1)
        predicted.extend(probabilities.argmax(1).tolist())
        confidences.extend(probabilities.max(1).values.tolist())
# A09: 혼동행렬(행=실제/열=예측)에서 클래스별 support/precision/recall/F1을 계산한다.
# support는 실제 표본 수, predicted_count는 예측 표본 수. 분모가 0이면 해당 지표를 0.0으로 둔다.
# macro 지표는 클래스의 단순 평균이다. 전체 정확도와 혼동하지 않는다.
cm = torch.zeros(2, 2, dtype=torch.long)
class_rows = []
# BEGIN A09
# TODO A09: 바로 위 요구사항에 맞게 구현하세요.
pass
# END A09
pd.DataFrame(class_rows, columns=["class_id", "name", "support", "correct", "precision", "recall", "f1"]).to_csv(out / "class_metrics.csv", index=False)
# A10: 실제 오답만 저장한다. 파일 순서는 valid.samples와 같고 경로는 data/ 기준 상대경로다.
# confidence는 모델의 예측 클래스 확률이며 정답 여부를 보증하지 않는다.
# 정답이 틀린 항목만 error_rows에 넣는다. 오답이 0개이면 헤더만 있는 CSV가 정상이다.
# 오답을 만들어내려고 라벨/예측을 조작하거나 test를 읽지 않는다.
error_rows = []
# BEGIN A10
# TODO A10: 바로 위 요구사항에 맞게 구현하세요.
pass
# END A10
pd.DataFrame(error_rows, columns=["file", "actual", "predicted", "confidence"]).to_csv(out / "error_samples.csv", index=False)
print("클래스별 지표 행 수:", len(class_rows), "실제 오답 수:", len(error_rows))
print(pd.DataFrame(history).round(4).to_string(index=False))
print("best epoch:", best_epoch)
print("혼동행렬 행=실제, 열=예측:\n", cm.tolist())
print("클래스별 정답 수:", cm.diag().tolist(), "/", cm.sum(1).tolist())
pd.DataFrame(history).to_csv(out / "cnn_history.csv", index=False)
pd.DataFrame(cm.numpy(), index=train.classes, columns=train.classes).to_csv(out / "confusion_matrix.csv")
pd.DataFrame(dict(file=[Path(p).name for p,_ in valid.samples], actual=actual, predicted=predicted)).to_csv(out / "cnn_predictions.csv", index=False)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

table = pd.DataFrame(history)
plt.figure(figsize=(7, 4))
plt.plot(table.epoch, table.train_loss, label="train (eval mode)")
plt.plot(table.epoch, table.valid_loss, label="valid")
plt.xlabel("Epoch")
plt.ylabel("Cross entropy")
plt.legend()
plt.tight_layout()
plt.savefig(out / "learning_curve.png", dpi=140)
plt.close()
torch.save(dict(state_dict=best_state, classes=train.classes, class_to_idx=train.class_to_idx,
                image_size=32, normalize=None, architecture="conv16_conv32_gap_fc2", best_epoch=best_epoch),
           out / "best_model.pt")
pd.DataFrame([dict(model="SmallCNN", trainable_params=5154, image_size=32, best_epoch=best_epoch,
                   valid_loss=best_loss, valid_accuracy=float(cm.diag().sum()/cm.sum()))]).to_csv(out / "model_comparison.csv", index=False)
print("CNN 결과 저장 완료. 06_transfer의 표는 입력 크기·학습량 차이를 함께 비교한다.")
