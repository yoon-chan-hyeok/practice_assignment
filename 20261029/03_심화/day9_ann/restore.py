"""실습 08: main.py가 만든 state_dict만 로드합니다. 새 프로세스 CPU에서 복원합니다."""
from pathlib import Path
import csv
import torch
from model import SimpleANN

base = Path(__file__).resolve().parent
with (base / "data" / "points.csv").open(encoding="utf-8",newline="") as f:
    valid_rows = [r for r in csv.DictReader(f) if r["split"] == "valid"]
X = torch.tensor([[float(r["x1"]),float(r["x2"])] for r in valid_rows])
model = SimpleANN()
# 직접 저장한 model_state.pt를 map_location="cpu", weights_only=True로 읽고 모델에 넣으세요.
# 먼저 같은 모델 구조를 만들었습니다. 인터넷에서 받은 출처 불명 파일은 읽지 마세요.
# >>> H10
# TODO H10: 위 요구사항을 읽고 이 블록을 완성하세요.
pass
# <<< H10
model.eval()
with torch.no_grad():
    predictions = model(X).argmax(dim=1).tolist()
with (base / "outputs" / "validation_predictions.csv").open(encoding="utf-8-sig",newline="") as f:
    saved = list(csv.DictReader(f))
print("ID 순서 동일:", [r["id"] for r in valid_rows] == [r["id"] for r in saved])
print("예측 동일:", predictions == [int(r["predicted"]) for r in saved])
print("서로 다른 CPU/GPU의 마지막 비트까지 동일함을 보장하는 검사는 아닙니다.")
