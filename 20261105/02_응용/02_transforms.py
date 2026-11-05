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
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

# 여기서는 [0,1] RGB 32×32로 학습한 교육용 source 가중치를 사용합니다.
# ImageNet ResNet18과 입력 변환을 섞지 않습니다.
transform = tr.Compose([tr.Resize((32, 32)), tr.ToTensor()])
from torchvision.models import ResNet18_Weights
from PIL import Image
weights = ResNet18_Weights.IMAGENET1K_V1  # Enum·변환 생성은 다운로드하지 않음
# TODO A02: Weight가 제공하는 transforms()를 가져오세요.
# BEGIN A02
official = tr.Compose([tr.ToTensor()])  # weights.transforms()로 바꾸세요.
# END A02
image = Image.open(sorted((DATA/"valid"/"circle").glob("*.png"))[0]).convert("RGB")
print("소형 source 입력:",tuple(transform(image).shape),"범위 [0,1]")
print("공식 ResNet 입력:",tuple(official(image).shape))
print("공식 Resize/Crop:", official.resize_size,official.crop_size)
print("공식 mean/std:", official.mean,official.std)
print("작은 source와 ImageNet의 Normalize를 서로 섞지 않습니다.")
