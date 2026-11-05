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
from PIL import Image, ImageDraw
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
# 제공된 8회 학습. 평가용 valid를 backward에 넣지 않습니다.
for epoch in range(8):
    optimizer.zero_grad()
    loss = criterion(model(X_train), y_train)
    loss.backward()
    optimizer.step()
with torch.no_grad():
    logits = model(X_valid)
    probabilities = logits.softmax(dim=1)
    predictions = logits.argmax(dim=1)

# TODO A05: 실제값과 예측값이 다른 행의 인덱스를 구하세요.
# BEGIN A05
indices = []  # 예측과 실제가 다른 인덱스를 구하세요.
# END A05
records=[]
for old in OUT.glob("error_*.png"):old.unlink()
for i in indices[:8]:
    image=Image.open(valid.samples[i][0]).convert("RGB").resize((192,192))
    tile=Image.new("RGB",(192,240),"white");tile.paste(image,(0,0));draw=ImageDraw.Draw(tile)
    draw.text((5,195),f"true: {valid.classes[y_valid[i]]}",fill="black")
    draw.text((5,210),f"pred: {valid.classes[predictions[i]]}",fill="black")
    draw.text((5,225),f"p={probabilities[i].max().item():.3f}",fill="black")
    tile.save(OUT/f"error_{i:03d}.png")
    records.append({"file":Path(valid.samples[i][0]).name,"actual":int(y_valid[i]),"predicted":int(predictions[i]),"confidence":probabilities[i].max().item()})
pd.DataFrame(records,columns=["file","actual","predicted","confidence"]).to_csv(OUT/"errors.csv",index=False)
print("전체 오답:",len(indices),"저장:",len(records),"없으면 생성하지 않음")
