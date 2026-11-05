"""Day14: 제공된 정상 이미지로 학습합니다. test는 읽지 않습니다."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import torch
from torch import nn
from torchvision.datasets import ImageFolder
from torchvision import transforms as tr
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix

torch.set_num_threads(1)
torch.manual_seed(14)
BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE

# 여기서는 [0,1] RGB 32×32로 학습한 교육용 source 가중치를 사용합니다.
# ImageNet ResNet18과 입력 변환을 섞지 않습니다.
transform = tr.Compose([tr.Resize((32, 32)), tr.ToTensor()])
train = ImageFolder(DATA / "train", transform=transform)
valid = ImageFolder(DATA / "valid", transform=transform)
X_train = torch.stack([train[i][0] for i in range(len(train))])
y_train = torch.tensor(train.targets, dtype=torch.long)
X_valid = torch.stack([valid[i][0] for i in range(len(valid))])
y_valid = torch.tensor(valid.targets, dtype=torch.long)
# 제공 부분: 0~8은 Backbone, 9는 새 3클래스 Head입니다.
model = nn.Sequential(
    nn.Conv2d(3, 8, 3, padding=1, bias=False), nn.BatchNorm2d(8), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(8, 16, 3, padding=1, bias=False), nn.BatchNorm2d(16), nn.ReLU(),
    nn.AdaptiveAvgPool2d((4, 4)), nn.Flatten(), nn.Linear(256, 3),
)
# 안전한 수치 배열만 읽습니다. Target 이미지로 사전학습한 파일이 아닙니다.
with np.load(DATA / "source_backbone.npz", allow_pickle=False) as saved:
    state = model.state_dict()
    state.update({name: torch.from_numpy(saved[name].copy()) for name in saved.files})
model.load_state_dict(state)
# requires_grad는 가중치 갱신, eval()은 BatchNorm 통계 사용 방식을 제어합니다.
for p in model.parameters():
    p.requires_grad = False
for p in model[9].parameters():
    p.requires_grad = True
model.eval()  # 고정 Backbone의 running 통계도 보존
optimizer = torch.optim.AdamW(model[9].parameters(), lr=0.01, weight_decay=0.0)
criterion = nn.CrossEntropyLoss()
# 오류 관찰용 초기 1회 학습. 07번 최종 8회 학습 모델과 구분합니다.
for epoch in range(1):
    optimizer.zero_grad()
    loss = criterion(model(X_train), y_train)
    loss.backward()
    optimizer.step()
with torch.no_grad():
    logits = model(X_valid)
    probabilities = logits.softmax(dim=1)
    predictions = logits.argmax(dim=1)

# TODO B05: 실제 y_valid와 predictions로 혼동행렬을 만드세요. 행=실제, 열=예측.
# BEGIN B05
matrix = np.zeros((3, 3), dtype=int)  # confusion_matrix 호출로 바꾸세요.
# END B05
print("혼동행렬:\n", matrix)
print(classification_report(y_valid, predictions, labels=[0, 1, 2], target_names=valid.classes, zero_division=0, digits=3))
errors = (predictions != y_valid).nonzero().flatten().tolist()
print("오답 개수:", len(errors))
for i in errors[:3]:
    print(Path(valid.samples[i][0]).name, "실제:", valid.classes[y_valid[i]], "예측:", valid.classes[predictions[i]])
