"""실습 07~08 응용: 06번 계획을 읽어 개발80으로 새 Pipeline을 학습하고 test20을 평가합니다."""
from pathlib import Path
import json
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"
plan = json.loads((OUT / "selection.json").read_text(encoding="utf-8"))
raw = pd.read_csv(HERE / "data/requests.csv").set_index("request_id")
ids = plan["split_ids"]
develop = raw.loc[ids["train"] + ids["valid"]]
test = raw.loc[ids["test"]]
X_develop, X_test = develop[plan["features"]].copy(), test[plan["features"]].copy()
NUM, CAT = plan["features"][:2], plan["features"][2:]
# 제공: 같은 행별 공식을 새 입력에도 적용합니다. 학습 통계는 아래 fit(develop)에서만 계산됩니다.
if plan["derived"]:
    for part in (X_develop, X_test):
        part["log_input_chars"] = np.log1p(part["input_chars"])
        part["chars_per_slot"] = part["input_chars"] / (1.0 + part["allowed_tools"])
    NUM = NUM + ["log_input_chars", "chars_per_slot"]
pre = ColumnTransformer([
    ("num", Pipeline([("imputer", SimpleImputer(strategy="median", keep_empty_features=True)), ("scaler", StandardScaler())]), NUM),
    ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent", keep_empty_features=True)),
                      ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))]), CAT),
])
model = Pipeline([("pre", pre), ("model", LogisticRegression(C=plan["C"], max_iter=plan["max_iter"]))])
# TODO A07a: 새 Pipeline을 X_develop·failed로 학습하세요. 기존 train 통계를 재사용하지 않고 개발80에서 새로 fit합니다.
pass
# TODO 끝
positive_column = model.classes_.tolist().index(1)
# TODO A07b: 확정 모델로 test의 실패 확률을 구하세요. test는 fit하지 않습니다.
probability = np.zeros(len(test))
# TODO 끝
prediction = (probability > plan["threshold"]).astype(int)
tn, fp, fn, tp = confusion_matrix(test["failed"], prediction, labels=[0, 1]).ravel()
metrics = {"n": len(test), "Accuracy": accuracy_score(test["failed"], prediction),
           "Precision": precision_score(test["failed"], prediction, zero_division=0),
           "Recall": recall_score(test["failed"], prediction, zero_division=0),
           "F1": f1_score(test["failed"], prediction, zero_division=0),
           "ROC_AUC": roc_auc_score(test["failed"], probability),
           "TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp), "actual_failed": int(test["failed"].sum())}
result = pd.DataFrame({"request_id": test.index, "actual": test["failed"].to_numpy(),
                       "probability_failed": probability, "predicted": prediction})
result.to_csv(OUT / "test_predictions.csv", index=False, encoding="utf-8-sig")
(OUT / "test_metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
print("확정 모델:", plan["selected"], "/ 학습80·최종20")
print(pd.DataFrame([metrics]).round(4).to_string(index=False))
print("오류 사례")
print(result.loc[result["actual"] != result["predicted"]].head(3).round(3).to_string(index=False))
print("저장: outputs/test_predictions.csv, test_metrics.json")
print("08번에서는 이 설정·원본을 그대로 재실행합니다. test를 보고 후보를 다시 고르지 않습니다.")
