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

results = []
for strategy in ["head", "partial"]:
    torch.manual_seed(14)  # 두 전략은 같은 source·Head 초기값·분할·8회 학습
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

    for p in model.parameters():
        p.requires_grad = False
    # TODO B03: 두 전략에서 Head(9)를 열고, partial일 때 두 번째 Conv(4)도 여세요.
    # BEGIN B03
    for p in model[9].parameters():
        p.requires_grad = True
    # partial에서 model[4]의 파라미터도 True로 바꾸는 코드를 추가하세요.
    # END B03
    model.eval()  # BN 통계는 두 전략 모두 고정합니다.
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.003, weight_decay=0.0)
    for epoch in range(8):
        optimizer.zero_grad()
        loss = nn.CrossEntropyLoss()(model(X_train), y_train)
        loss.backward()
        optimizer.step()
    with torch.no_grad():
        pred = model(X_valid).argmax(1)
    results.append([strategy, sum(p.numel() for p in model.parameters() if p.requires_grad), accuracy_score(y_valid, pred)])
print(pd.DataFrame(results, columns=["strategy", "trainable", "valid_accuracy"]).round(4).to_string(index=False))
