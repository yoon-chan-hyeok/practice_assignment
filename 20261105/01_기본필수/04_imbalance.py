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

# 손으로 읽는 지표 예제입니다. 모델의 실제 예측이라고 주장하지 않습니다.
y_true = [0] * 12 + [1] * 6 + [2] * 3
y_pred = [0] * 21
print("클래스 수:", [y_true.count(i) for i in range(3)])
print("Accuracy:", round(accuracy_score(y_true, y_pred), 4))
# TODO B04: f1_score에 average="macro", labels=[0,1,2], zero_division=0을 넣으세요.
# BEGIN B04
macro = 0.0  # f1_score 계산으로 바꾸세요.
# END B04
print("Macro F1:", round(macro, 4))
print(classification_report(y_true, y_pred, labels=[0, 1, 2], target_names=["circle", "square", "triangle"], zero_division=0, digits=3))
