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

history = []
best_loss = float("inf")
for epoch in range(1, 9):
    optimizer.zero_grad()
    loss = criterion(model(X_train), y_train)
    # TODO B07: 역전파와 Optimizer 갱신을 수행하세요.
    # BEGIN B07
    pass  # loss.backward()와 optimizer.step() 두 문장을 작성하세요.
    # END B07
    with torch.no_grad():
        valid_loss = criterion(model(X_valid), y_valid).item()
    history.append({"epoch": epoch, "valid_loss": valid_loss})
    if valid_loss < best_loss:
        best_loss = valid_loss
        best_epoch = epoch
        best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
model.load_state_dict(best_state)
with torch.no_grad():
    logits = model(X_valid)
    probabilities = logits.softmax(1)
    # TODO B08: 각 행의 가장 큰 logit 열을 예측 라벨로 고르세요.
    # BEGIN B08
    predictions = torch.zeros(len(valid), dtype=torch.long)  # argmax로 바꾸세요.
    # END B08
metrics = {"accuracy": accuracy_score(y_valid, predictions), "macro_f1": f1_score(y_valid, predictions, labels=[0,1,2], average="macro", zero_division=0), "best_epoch": best_epoch, "valid_n": len(valid), "source": "synthetic_source_pretraining", "test_used": False}
pd.DataFrame([metrics]).to_csv(OUT / "metrics.csv", index=False)
pd.DataFrame(history).to_csv(OUT / "history.csv", index=False)
pd.DataFrame({"file": [Path(p).name for p,_ in valid.samples], "actual": y_valid.numpy(), "predicted": predictions.numpy(), "confidence": probabilities.max(1).values.numpy()}).to_csv(OUT / "predictions.csv", index=False)
# TODO B09: metrics를 UTF-8 JSON 문자열로 저장하세요. 아래 제공된 경로를 사용합니다.
# BEGIN B09
pass  # write_text로 metrics JSON을 저장하세요.
# END B09
pd.DataFrame(confusion_matrix(y_valid, predictions, labels=[0,1,2]), index=valid.classes, columns=valid.classes).to_csv(OUT / "confusion.csv")
for old in OUT.glob("project_error_*.png"):
    old.unlink()
errors = (predictions != y_valid).nonzero().flatten().tolist()
for i in errors[:8]:
    image = (X_valid[i].permute(1,2,0).numpy()*255).astype(np.uint8)
    cv2.imwrite(str(OUT / f"project_error_{i:02d}.png"), cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
index = errors[0] if errors else 0
# hook 대신 Sequential을 둘로 나눕니다. 관심 클래스의 logit을 미분합니다.
image = X_valid[index:index + 1].clone().requires_grad_(True)
features = model[:7](image)
logits_one = model[7:](features)
target = int(logits_one.argmax(1).item())
gradient = torch.autograd.grad(logits_one[0, target], features)[0]
weights = gradient.mean(dim=(2, 3), keepdim=True)
cam = (weights * features).sum(dim=1).relu()
cam = torch.nn.functional.interpolate(cam.unsqueeze(1), size=(32, 32), mode="bilinear", align_corners=False)[0, 0]
cam = cam.detach().numpy()
cam = cam / max(float(cam.max()), 1e-8)  # 양의 반응이 없으면 0 지도를 유지
rgb = (X_valid[index].permute(1, 2, 0).numpy() * 255).astype(np.uint8)
heat_bgr = cv2.applyColorMap(np.uint8(cam * 255), cv2.COLORMAP_JET)
overlay = cv2.addWeighted(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), 0.6, heat_bgr, 0.4, 0)

cv2.imwrite(str(OUT / "project_cam.png"), cv2.resize(overlay,(256,256)))
print(json.dumps(metrics,ensure_ascii=False,sort_keys=True))
print("오답 수:",len(errors),"예측 행:",len(valid),"test 사용: False")
