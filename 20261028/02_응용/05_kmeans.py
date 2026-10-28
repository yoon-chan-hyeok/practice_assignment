"""실습 05 응용: train 수치2열만 결측 대체·표준화하여 K=3으로 묶습니다."""
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

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
cluster = Pipeline([("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                    ("kmeans", KMeans(n_clusters=3, n_init=10, random_state=42))])
# TODO A05: 수치2열만으로 cluster를 학습하세요. failed나 elapsed_ms를 넣지 않습니다.
pass
# TODO 끝
labels = cluster["kmeans"].labels_
z = cluster[:-1].transform(X_train[NUM])
centers = cluster["scaler"].inverse_transform(cluster["kmeans"].cluster_centers_)
profile = pd.DataFrame(centers, columns=NUM)
profile.insert(0, "cluster", range(3))
profile["n"] = np.bincount(labels, minlength=3)
profile.to_csv(OUT / "cluster_profile.csv", index=False, encoding="utf-8-sig")
pd.DataFrame({"request_id": train_ids, "cluster": labels}).to_csv(OUT / "cluster_assignments.csv", index=False, encoding="utf-8-sig")
print(profile.round(3).to_string(index=False))
print("silhouette(표준화 공간):", round(silhouette_score(z, labels), 3))
print("군집 번호에는 실패·성공·우열의 뜻이 없습니다.")
