"""실습 07~08: 06번의 설정을 그대로 읽어 개발 16건으로 학습하고 test 4건을 최종 평가합니다."""
from pathlib import Path
import pandas as pd
import numpy as np
import json
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
HERE = Path(__file__).resolve().parent
# 제공: 06번을 먼저 완료하세요. 이 프로그램은 CV·설정 선택을 다시 하지 않습니다.
plan = json.loads((HERE / "selection.json").read_text(encoding="utf-8"))
raw = pd.read_csv(HERE / "requests.csv").set_index("request_id")
develop = raw.loc[plan["train_ids"] + plan["valid_ids"]].copy()
test = raw.loc[plan["test_ids"]].copy()
# 제공: 행별 공식은 새 요청에도 동일하게 적용합니다. test로 통계나 설정을 학습하지 않습니다.
for table in (develop, test):
    table["log_input_chars"] = np.log1p(table["input_chars"])
model = DecisionTreeClassifier(max_depth=plan["max_depth"], random_state=plan["random_state"])
# TODO B07a: 개발 자료 16건의 선택된 입력과 failed로 학습하세요. test는 넣지 않습니다.
pass
# TODO 끝
# 0·1 두 클래스가 있는 정상 자료입니다. classes_에서 양성 1의 위치를 확인합니다.
positive_column = model.classes_.tolist().index(1)
# TODO B07b: test의 실패 확률을 구하세요. predict_proba의 positive_column 열만 선택합니다.
probability = np.zeros(len(test))
# TODO 끝
prediction = (probability > plan["threshold"]).astype(int)
# TODO B07c: F1에는 0/1 예측값, AUC에는 실패 확률을 넣으세요.
f1 = auc = 0.0
# TODO 끝
metrics = {"n": len(test), "Accuracy": accuracy_score(test["failed"], prediction),
           "Precision": precision_score(test["failed"], prediction, zero_division=0),
           "Recall": recall_score(test["failed"], prediction, zero_division=0),
           "F1": f1, "ROC_AUC": auc, "TP": int(((test["failed"] == 1) & (prediction == 1)).sum()),
           "actual_failed": int(test["failed"].sum()), "threshold": plan["threshold"]}
result = pd.DataFrame({"request_id": test.index, "actual": test["failed"].to_numpy(),
                       "probability_failed": probability, "predicted": prediction})
result.to_csv(HERE / "test_predictions.csv", index=False, encoding="utf-8-sig")
(HERE / "test_metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
print("개발/최종평가:", len(develop), len(test))
print(result.round(3).to_string(index=False))
print("혼동행렬:", confusion_matrix(test["failed"], prediction, labels=[0, 1]).tolist())
print(f"Accuracy={metrics['Accuracy']:.3f}, Precision={metrics['Precision']:.3f}, Recall={metrics['Recall']:.3f}, F1={f1:.3f}, AUC={auc:.3f}")
print("저장: test_predictions.csv, test_metrics.json")
print("08번은 이 설정 그대로 재실행합니다. test를 보고 06번 설정을 다시 고르지 않습니다.")
