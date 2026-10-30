"""실습 07~08: 앞 실습을 한 파일로 연결하고 환경·학습·평가 결과를 저장합니다."""

from pathlib import Path
import csv
import json
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader

base = Path(__file__).resolve().parent
out = base / "outputs"
out.mkdir(exist_ok=True)
with (base / "data" / "points.csv").open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
train_rows = [r for r in rows if r["split"] == "train"]
valid_rows = [r for r in rows if r["split"] == "valid"]
X_train = torch.tensor([[float(r["x1"]), float(r["x2"])] for r in train_rows])
y_train = torch.tensor([int(r["label"]) for r in train_rows], dtype=torch.long)
X_valid = torch.tensor([[float(r["x1"]), float(r["x2"])] for r in valid_rows])
y_valid = torch.tensor([int(r["label"]) for r in valid_rows], dtype=torch.long)
# test 40건은 모델에 전달하지 않습니다. 순서를 바꾸거나 다시 분할하지 않습니다.
torch.manual_seed(42)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
loader = DataLoader(TensorDataset(X_train, y_train), batch_size=32, shuffle=True,
                    generator=torch.Generator().manual_seed(43), num_workers=0)
model = nn.Sequential(nn.Linear(2, 8), nn.ReLU(), nn.Linear(8, 2)).to(device)
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
Xv, yv = X_valid.to(device), y_valid.to(device)
Xt, yt = X_train.to(device), y_train.to(device)
history = []

for epoch in range(81):
    if epoch > 0:
        model.train()
        for xb, yb in loader:
            xb, yb = xb.to(device), yb.to(device)
            optimizer.zero_grad()
            loss = loss_fn(model(xb), yb)
            # 각 batch에서 backward와 step을 연결하세요.
            # train 자료만 loader에 들어갑니다. valid로 backward하거나 학습하지 마세요.
            # >>> A07
            # TODO A07: 위 요구사항을 읽고 이 블록을 완성하세요.
            pass
            # <<< A07
    # epoch=0은 학습 전입니다. 로그는 갱신이 끝난 동일 모델로 측정합니다.
    if epoch % 10 == 0:
        model.eval()
        with torch.no_grad():
            train_loss = loss_fn(model(Xt), yt).item()
            logits = model(Xv)
            valid_loss = loss_fn(logits, yv).item()
            accuracy = (logits.argmax(dim=1) == yv).float().mean().item()
        history.append([epoch, train_loss, valid_loss, accuracy])
        print(epoch, round(train_loss, 6), round(valid_loss, 6), round(accuracy, 4))

with (out / "training_history.csv").open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["epoch", "train_loss_eval", "valid_loss", "valid_accuracy"])
    writer.writerows(history)

model.eval()
with torch.no_grad():
    logits = model(Xv)
    # logits의 클래스 축에서 가장 큰 점수의 인덱스를 구하세요.
    # CSV로 저장하기 전에 CPU로 옮깁니다. y_valid의 순서는 그대로 유지하세요.
    # >>> A08
    # TODO A08: 위 요구사항을 읽고 이 블록을 완성하세요.
    predictions = torch.zeros(len(y_valid), dtype=torch.long)
    # <<< A08
metrics = {"device": str(device), "torch": str(torch.__version__), "epochs": 80,
           "train_rows": len(train_rows), "valid_rows": len(valid_rows), "test_used": False,
           "initial_train_loss": history[0][1], "final_train_loss": history[-1][1],
           "valid_loss": history[-1][2], "valid_accuracy": history[-1][3]}
(out / "final_metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
with (out / "validation_predictions.csv").open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f); writer.writerow(["id", "actual", "predicted"])
    writer.writerows((r["id"], int(y), int(p)) for r, y, p in zip(valid_rows, y_valid, predictions))
(out / "gpu_check.txt").write_text(
    f"torch={torch.__version__}\ncuda_build={torch.version.cuda}\n"
    f"cuda_available={torch.cuda.is_available()}\nselected_device={device}\n", encoding="utf-8")
print("생성: outputs의 환경·학습·검증 결과")

# 추가 A10: valid의 실제값과 예측을 비교해 오답 목록을 만드세요.
# 입력: valid_rows, y_valid, predictions는 동일한 40개 ID 순서입니다.
# 반환 형식: errors=[(요청ID, 실제정답int, 예측int), ...].
# 조건: 실제값과 예측이 다른 행만 포함하고 원래 valid 순서를 유지합니다.
# 금지: test 자료 사용, 정답 변경, 오답이 없을 때 가상의 오답 추가.
# 완료: 오류 행 수 = 40 - 맞힌 개수, 저장 파일은 헤더를 포함합니다.
# >>> A10
# TODO A10: 실제 오답 행만 ID와 함께 수집하세요.
errors = []
# <<< A10
with (out / "validation_errors.csv").open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "actual", "predicted"])
    writer.writerows(errors)
print("valid 오답 수:", len(errors))
