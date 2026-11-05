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
import cv2
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

# 실제 정답/오답 예를 각각 최대 1개 고릅니다. 없으면 억지로 만들지 않습니다.
selected = []
for kind, mask in [("correct", predictions == y_valid), ("wrong", predictions != y_valid)]:
    indices = mask.nonzero().flatten().tolist()
    if indices:
        selected.append((kind, indices[0]))
    else:
        print(kind, "사례 없음: 지표 그대로 보고")
for kind, index in selected:
    image = X_valid[index:index + 1].clone().requires_grad_(True)
    features = model[:7](image)
    one = model[7:](features)
    target = int(one.argmax(1).item())
    gradient = torch.autograd.grad(one[0, target], features)[0]
    weights = gradient.mean(dim=(2, 3), keepdim=True)
    # TODO B06: 채널 가중합에 relu()를 적용해 양의 반응만 남기세요.
    # BEGIN B06
    cam = torch.zeros_like(features[:, 0])  # 채널 가중합과 relu로 바꾸세요.
    # END B06
    cam = torch.nn.functional.interpolate(cam.unsqueeze(1), size=(32,32), mode="bilinear", align_corners=False)[0,0].detach().numpy()
    cam = cam / max(float(cam.max()), 1e-8)
    rgb = (X_valid[index].permute(1,2,0).numpy()*255).astype(np.uint8)
    heat = cv2.applyColorMap(np.uint8(cam*255), cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR),0.6,heat,0.4,0)
    cv2.imwrite(str(OUT / f"cam_{kind}.png"), cv2.resize(overlay,(256,256)))
    print(kind, Path(valid.samples[index][0]).name, "target:", valid.classes[target], "CAM:", cam.shape)
# 이 그림은 점수에 대한 반응입니다. 원인·정답 증명이 아닙니다.
