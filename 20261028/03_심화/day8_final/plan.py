"""실습 06 심화: train CV로 선택하고 설정을 저장합니다. test 입력·정답은 선택하지 않습니다."""
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

import json
from sklearn.base import clone
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import f1_score
from preprocessing import CANDIDATES

# 제공: 최종 평가 파일이 이미 있으면 기존 계획을 보존합니다. 보안 잠금이 아닌 실습용 진행 안내입니다.
if (OUT / "test_metrics.json").exists():
    print("최종 평가 이후에는 선택을 다시 하지 않습니다. 기존 selection.json으로 main.py를 재실행하세요.")
else:
    folds = list(StratifiedKFold(n_splits=5, shuffle=True, random_state=42).split(X_train, y_train))
    rows, fold_rows = [], []
    for name, prototype in CANDIDATES.items():
        model = clone(prototype)
        # TODO H06: 각 후보 Pipeline을 동일 train 5-fold로 비교하세요. 미리 전체 train을 변환하지 않습니다.
        scores = np.zeros(5)
        # TODO 끝
        model.fit(X_train, y_train)
        rows.append({"model": name, "CV_F1": scores.mean(), "CV_std": scores.std(),
                     "valid_F1": f1_score(y_valid, model.predict(X_valid), zero_division=0)})
        for number, value in enumerate(scores, start=1):
            fold_rows.append({"model": name, "fold": number, "F1": value})
    result = pd.DataFrame(rows)
    selected = result.loc[result["CV_F1"].idxmax(), "model"]
    test_ids = manifest.loc[manifest["split"] == "test"].sort_values("position")["request_id"].tolist()
    plan = {"selected": selected, "candidate_order": list(CANDIDATES),
            "features": FEATURES, "derived": selected == "Logistic_FE", "threshold": 0.5,
            "rule": "score > threshold", "positive_label": 1,
            "selection": "train60 5-fold mean F1 max; exact tie: candidate order",
            "cv_splits": 5, "cv_shuffle": True, "cv_random_state": 42,
            "train_ids": train_ids, "valid_ids": valid_ids, "test_ids": test_ids,
            "model_params": CANDIDATES[selected]["model"].get_params(deep=False)}
    result.to_csv(OUT / "cv_comparison.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(fold_rows).to_csv(OUT / "cv_scores.csv", index=False, encoding="utf-8-sig")
    result.loc[result["model"].isin(["Logistic", "Logistic_FE"])].to_csv(OUT / "feature_comparison.csv", index=False, encoding="utf-8-sig")
    (OUT / "selection.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(result.round(4).to_string(index=False))
    print("선택:", selected, "/ 계획 저장 완료 / test20 미평가")
