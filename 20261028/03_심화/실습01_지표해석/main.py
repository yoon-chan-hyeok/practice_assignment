"""실습 01 심화: 지표와 업무 비용을 함께 읽습니다. 기존 응용 수준의 짧은 비교입니다."""
from pathlib import Path
import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
OUT = Path(__file__).resolve().parent / "outputs"
OUT.mkdir(exist_ok=True)
y = [0]*14 + [1]*6
predictions = {"example": [0]*10 + [1]*4 + [0]*4 + [1]*2, "all_success": [0]*20}
rows = []
for name, pred in predictions.items():
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    # TODO H01: FP 비용1, FN 비용5라는 가정으로 총비용을 계산하세요.
    cost = 0
    # TODO 끝
    rows.append({"model": name, "Accuracy": accuracy_score(y, pred),
                 "Precision": precision_score(y, pred, zero_division=0),
                 "Recall": recall_score(y, pred, zero_division=0),
                 "F1": f1_score(y, pred, zero_division=0), "FP": fp, "FN": fn,
                 "assumed_cost": cost})
result = pd.DataFrame(rows)
result.to_csv(OUT / "metric_comparison.csv", index=False, encoding="utf-8-sig")
print(result.round(3).to_string(index=False))
print("가정: 오탐 1회 비용1, 실제 실패를 놓친 비용5. 비용 단위는 임의 점수입니다.")
