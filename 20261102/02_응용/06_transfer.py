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

from torchvision.models import resnet18, ResNet18_Weights

weights = ResNet18_Weights.IMAGENET1K_V1
train = datasets.ImageFolder(root / "data" / "train", transform=weights.transforms())
valid = datasets.ImageFolder(root / "data" / "valid", transform=weights.transforms())
# 1 epoch는 학습 경로 점검용이다. 이 숫자로 일반화 성능의 우열을 단정하지 않는다.
rows = []
for mode in ["head", "partial"]:
    torch.manual_seed(42)
    model = resnet18(weights=weights)  # 가중치가 없으면 공식 다운로드. 무작위 초기화로 대체하지 않는다.
    for param in model.parameters():
        param.requires_grad = False
    model.fc = nn.Linear(model.fc.in_features, 2)
    groups = [{"params": model.fc.parameters(), "lr": 0.001}]
    if mode == "partial":
        # BEGIN A06
        # TODO A06: partial일 때만 layer4의 미분을 켠다.
        for param in model.layer4.parameters():
            param.requires_grad = False
        # END A06
        groups.append({"params": model.layer4.parameters(), "lr": 0.0001})
    optimizer = torch.optim.AdamW(groups, weight_decay=0.0001)
    train_loader = DataLoader(train, batch_size=4, shuffle=True, num_workers=0,
                              generator=torch.Generator().manual_seed(42))
    model.eval()  # BN running 통계는 두 조건 모두 고정한다.
    model.fc.train()
    if mode == "partial":
        model.layer4.train()
        for layer in model.layer4.modules():
            if isinstance(layer, nn.BatchNorm2d):
                layer.eval()
    start = time.perf_counter()
    for images, labels in train_loader:
        optimizer.zero_grad()
        nn.functional.cross_entropy(model(images), labels).backward()
        optimizer.step()
    training_seconds = time.perf_counter() - start
    model.eval()
    total_loss, correct, count = 0.0, 0, 0
    with torch.no_grad():
        for images, labels in DataLoader(valid, batch_size=4):
            logits = model(images)
            total_loss += nn.functional.cross_entropy(logits, labels).item()*len(labels)
            correct += (logits.argmax(1)==labels).sum().item()
            count += len(labels)
    rows.append(dict(mode=mode, pretrained=weights.name, image_size=224, epochs=1,
                     trainable_params=sum(p.numel() for p in model.parameters() if p.requires_grad),
                     valid_loss=total_loss/count, valid_accuracy=correct/count, training_seconds=training_seconds))
print(pd.DataFrame(rows).drop(columns="training_seconds").round(4).to_string(index=False))
pd.DataFrame(rows).to_csv(out / "transfer_comparison.csv", index=False)
