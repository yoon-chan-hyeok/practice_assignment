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
# TODO B02: 256개 특징에서 3개 logit을 출력하는 새 Linear Head를 만드세요.
# BEGIN B02
model[9] = nn.Linear(256, 1)  # 출력 개수를 고치세요.
# END B02
print("source 종류: 별도 합성 이미지로 사전학습한 TinyShapeCNN")
print("학습 파라미터:", sum(p.numel() for p in model.parameters() if p.requires_grad))
print("출력 shape:", tuple(model.eval()(torch.zeros(2, 3, 32, 32)).shape))
# PPT ResNet18의 구조도 다운로드 없이 확인합니다. 이것은 '전이학습 성능'이 아닙니다.
from torchvision.models import resnet18
resnet = resnet18(weights=None)
for p in resnet.parameters():
    p.requires_grad = False
resnet.fc = nn.Linear(resnet.fc.in_features, 3)
print("ResNet18 구조 확인용 Head 파라미터:", sum(p.numel() for p in resnet.parameters() if p.requires_grad))
print("주의: 위 ResNet18은 구조만 확인했습니다. ImageNet 학습 결과가 아닙니다.")
