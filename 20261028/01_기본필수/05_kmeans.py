"""실습 05: train 12건의 글자 수 하나로 두 묶음을 만듭니다."""
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
HERE = Path(__file__).resolve().parent
raw = pd.read_csv(HERE / "requests.csv")
# 제공: 앞 수업과 같은 seed·층화·행 순서입니다. test 4건은 마지막 평가 전까지 보관합니다.
develop, test = train_test_split(raw, test_size=0.2, stratify=raw["failed"], random_state=42)
train, valid = train_test_split(develop, test_size=0.25, stratify=develop["failed"], random_state=42)

from sklearn.cluster import KMeans
# 같은 단위인 한 열만 사용하므로 여기서는 표준화를 생략합니다. failed·elapsed_ms는 넣지 않습니다.
model = KMeans(n_clusters=2, n_init=10, random_state=42)
# TODO B05: KMeans를 train의 input_chars 한 열로 학습하세요. 정답 y는 전달하지 않습니다.
pass
# TODO 끝
result = train[["request_id", "input_chars"]].copy()
result["cluster"] = model.labels_
print("군집별 개수:", result["cluster"].value_counts().sort_index().to_dict())
print("중심(글자):", model.cluster_centers_.round(1).ravel().tolist())
result.to_csv(HERE / "clusters.csv", index=False, encoding="utf-8-sig")
print("저장: clusters.csv (군집 번호는 성공·실패 라벨이 아닙니다.)")
