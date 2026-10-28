"""실습 04 응용: 행별 특성 두 개만 추가하고 같은 Logistic·5-fold로 비교합니다."""
from pathlib import Path
import pandas as pd
import numpy as np
HERE = Path(__file__).resolve().parent
raw = pd.read_csv(HERE / "data/requests.csv").set_index("request_id")
manifest = pd.read_csv(HERE / "data/split_manifest.csv")
train_ids = manifest.loc[manifest["split"] == "train"].sort_values("position")["request_id"].tolist()
valid_ids = manifest.loc[manifest["split"] == "valid"].sort_values("position")["request_id"].tolist()
train, valid = raw.loc[train_ids].copy(), raw.loc[valid_ids].copy()
FEATURES = ["input_chars", "allowed_tools", "task_type", "priority"]
NUM, CAT = FEATURES[:2], FEATURES[2:]
X_train, X_valid = train[FEATURES].copy(), valid[FEATURES].copy()
y_train, y_valid = train["failed"], valid["failed"]
OUT = HERE / "outputs"
OUT.mkdir(exist_ok=True)
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
# 제공: 모든 평균·중앙값·범주 목록은 Pipeline.fit의 학습 부분에서만 결정됩니다.
pre = ColumnTransformer([
    ("num", Pipeline([("imputer", SimpleImputer(strategy="median", keep_empty_features=True)),
                      ("scaler", StandardScaler())]), NUM),
    ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent", keep_empty_features=True)),
                      ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))]), CAT),
])

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import f1_score
from sklearn.base import clone
# TODO A04: train·valid에 log_input_chars와 chars_per_slot을 추가하세요. 자기 행만 사용하고 NaN은 다음 Pipeline에서 처리합니다.
pass
# TODO 끝
folds = list(StratifiedKFold(n_splits=5, shuffle=True, random_state=42).split(X_train, y_train))
choices = {"Logistic": NUM, "Logistic_FE": NUM + ["log_input_chars", "chars_per_slot"]}
rows = []
for name, numeric_columns in choices.items():
    current_pre = clone(pre)
    # 제공: 파생 열이 있을 때 수치 경로에만 추가합니다. 범주 경로는 바꾸지 않습니다.
    current_pre.transformers[0] = ("num", current_pre.transformers[0][1], numeric_columns)
    model = Pipeline([("pre", current_pre), ("model", LogisticRegression(C=1, max_iter=1000))])
    scores = cross_val_score(model, X_train, y_train, cv=folds, scoring="f1", n_jobs=1)
    model.fit(X_train, y_train)
    rows.append({"model": name, "CV_F1": scores.mean(), "CV_std": scores.std(),
                 "valid_F1": f1_score(y_valid, model.predict(X_valid), zero_division=0)})
result = pd.DataFrame(rows)
result.to_csv(OUT / "feature_comparison.csv", index=False, encoding="utf-8-sig")
print(result.round(4).to_string(index=False))
print("CV는 선택용, valid는 진단용입니다. test는 아직 보지 않습니다.")
