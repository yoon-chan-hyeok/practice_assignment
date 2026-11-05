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

# TODO B01: ImageFolder로 train 폴더를 읽으세요. root는 필수 경로입니다.
# BEGIN B01
train = ImageFolder(DATA / "valid")  # train 폴더로 바꾸세요.
# END B01
print("class_to_idx:", train.class_to_idx)
for split in ["train", "valid", "test"]:
    dataset = ImageFolder(DATA / split)
    counts = [dataset.targets.count(i) for i in range(3)]
    print(split, "개수:", counts, "같은 매핑:", dataset.class_to_idx == train.class_to_idx)
# test는 파일명·라벨 매핑만 확인했습니다. 모델 예측에는 사용하지 않습니다.
