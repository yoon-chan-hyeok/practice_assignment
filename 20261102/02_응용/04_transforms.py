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

from PIL import Image, ImageDraw

path = sorted((root / "data" / "train" / "horizontal").glob("*.png"))[0]
image = Image.open(path).convert("RGB")
# 좌우반전은 가로·세로 줄무늬 라벨을 보존한다. 90도 회전은 라벨을 바꾸므로 사용하지 않는다.
train_transform = transforms.Compose([
    transforms.Resize((64, 64)), transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10), transforms.ColorJitter(brightness=0.15), transforms.ToTensor(),
])
# BEGIN A04
# TODO A04: valid에는 Resize와 ToTensor만 적용한다.
valid_transform = train_transform
# END A04
augmented = [train_transform(image) for _ in range(3)]
v1, v2 = valid_transform(image), valid_transform(image)
canvas = Image.new("RGB", (4*128, 150), "white")
draw = ImageDraw.Draw(canvas)
for i, tensor in enumerate([v1]+augmented):
    canvas.paste(transforms.ToPILImage()(tensor).resize((128,128)), (128*i,22))
    draw.text((128*i+5,4), "valid" if i==0 else f"train {i}", fill="black")
canvas.save(out / "augmentation_preview.png")
print("valid 동일:", torch.equal(v1, v2))
print("shape:", tuple(v1.shape))
print("train 3개 동일 여부:", torch.equal(augmented[0], augmented[1]))
