"""실습 07: 확정 계획을 읽고 새 Pipeline을 개발80으로 학습하여 최종 평가합니다."""
from pathlib import Path
import json
import sys
import pandas as pd
import numpy as np
import sklearn
import xgboost
import joblib
from sklearn.base import clone
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from preprocessing import CANDIDATES, FEATURES, NUM
from evaluate import summarize

HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"
plan = json.loads((OUT / "selection.json").read_text(encoding="utf-8"))
raw = pd.read_csv(HERE / "data/requests.csv").set_index("request_id")
develop = raw.loc[plan["train_ids"] + plan["valid_ids"]]
X_develop = develop[plan["features"]]
# 제공: CV 때 fit된 모델을 재사용하지 않습니다. 같은 확정 파라미터의 새 Pipeline을 만듭니다.
model = clone(CANDIDATES[plan["selected"]])
model["model"].set_params(**plan["model_params"])
# TODO H07a: 확정 모델을 개발80의 입력과 정답으로 학습하세요.
pass
# TODO 끝
# 설정 저장·개발 학습 후에만 test 입력과 정답을 선택합니다.
test = raw.loc[plan["test_ids"]]
X_test = test[plan["features"]]
positive_column = model.classes_.tolist().index(1)
# TODO H07b: 실패1의 확률을 구하세요. Feature Engineering도 저장될 Pipeline 안에서 적용됩니다.
probability = np.zeros(len(test))
# TODO 끝
prediction = (probability > plan["threshold"]).astype(int)
metrics = summarize(test["failed"], prediction, probability)
result = pd.DataFrame({"request_id": X_test.index, "actual": test["failed"].to_numpy(),
                       "probability_failed": probability, "predicted": prediction})
result.to_csv(OUT / "test_predictions.csv", index=False, encoding="utf-8-sig")
result.loc[result["actual"] != result["predicted"]].to_csv(OUT / "error_cases.csv", index=False, encoding="utf-8-sig")
(OUT / "test_metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
# 직접 만든 Pipeline만 저장합니다. 외부의 불명확한 joblib/pickle 파일은 열지 않습니다.
joblib.dump(model, OUT / "pipeline.joblib")
environment = {"python": sys.version.split()[0], "numpy": np.__version__, "pandas": pd.__version__,
               "scikit-learn": sklearn.__version__, "xgboost": xgboost.__version__}
(OUT / "environment.json").write_text(json.dumps(environment, indent=2), encoding="utf-8")
# 제공: 군집은 train60 수치2열만 사용하며 최종 분류의 선택 기준과는 분리합니다.
X_cluster = raw.loc[plan["train_ids"], NUM]
cluster = Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler()),
                    ("cluster", KMeans(n_clusters=3, n_init=10, random_state=42))])
cluster.fit(X_cluster)
labels = cluster["cluster"].labels_
centers = cluster["scaler"].inverse_transform(cluster["cluster"].cluster_centers_)
profile = pd.DataFrame(centers, columns=NUM)
profile.insert(0, "cluster", range(3))
profile["n"] = np.bincount(labels, minlength=3)
profile.to_csv(OUT / "cluster_profile.csv", index=False, encoding="utf-8-sig")
cluster_score = silhouette_score(cluster[:-1].transform(X_cluster), labels)
print("확정 모델:", plan["selected"], "/ 개발80·최종20")
print(pd.DataFrame([metrics]).round(4).to_string(index=False))
print("K=3 군집")
print(profile.round(3).to_string(index=False))
print("군집 silhouette:", round(cluster_score, 3))
print("저장: outputs/test_predictions.csv, test_metrics.json, pipeline.joblib 등")
print("최종 성능을 본 뒤 다시 탐색하지 않습니다. 다음은 restore.py로 재현 확인입니다.")
