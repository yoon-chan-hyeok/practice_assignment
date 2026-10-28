"""실습 03 심화: 회귀 Pipeline 두 개를 같은 KFold로 비교합니다."""
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
pre = ColumnTransformer([
    ("num", Pipeline([("imputer", SimpleImputer(strategy="median", keep_empty_features=True)),
                      ("scaler", StandardScaler())]), NUM),
    ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent", keep_empty_features=True)),
                      ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))]), CAT),
])

from sklearn.base import clone
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import KFold, cross_val_score
folds = list(KFold(n_splits=5, shuffle=True, random_state=42).split(X_train))
rows = []
for name, estimator in [("Linear", LinearRegression()), ("KNN15", KNeighborsRegressor(n_neighbors=15))]:
    model = Pipeline([("pre", clone(pre)), ("model", estimator)])
    # TODO H03: 같은 folds로 음수 RMSE 점수를 구한 뒤 부호를 되돌리세요.
    rmse = np.zeros(5)
    # TODO 끝
    for number, value in enumerate(rmse, start=1):
        rows.append({"model": name, "fold": number, "RMSE_ms": value})
result = pd.DataFrame(rows)
result.to_csv(OUT / "regression_cv.csv", index=False, encoding="utf-8-sig")
print(result.round(2).to_string(index=False))
print("평균 RMSE(ms)")
print(result.groupby("model", sort=False)["RMSE_ms"].mean().round(2).to_string())
print("회귀 교차검증의 정답은 elapsed_ms입니다. 입력에 elapsed_ms를 포함하지 않습니다.")
