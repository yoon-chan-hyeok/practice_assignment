"""실습 06 응용: 04번에서 만든 CV 표만 읽어 선택하고 평가 계획을 기록합니다."""
from pathlib import Path
import pandas as pd
import json
HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"
# 먼저 04_features.py를 완료하세요. valid_F1을 이용해 후보를 재선택하지 않습니다.
table = pd.read_csv(OUT / "feature_comparison.csv")
# TODO A06: CV_F1이 가장 큰 행의 model 이름을 선택하세요. 정확한 동점은 표의 첫 후보를 사용합니다.
selected = "Logistic"
# TODO 끝
manifest = pd.read_csv(HERE / "data/split_manifest.csv")
ids = {name: manifest.loc[manifest["split"] == name].sort_values("position")["request_id"].tolist()
       for name in ["train", "valid", "test"]}
plan = {"selected": selected, "C": 1, "max_iter": 1000,
        "features": ["input_chars", "allowed_tools", "task_type", "priority"],
        "derived": selected == "Logistic_FE", "threshold": 0.5,
        "rule": "score > threshold", "positive_label": 1,
        "selection": "train60 5-fold mean F1; exact tie: Logistic first", "split_ids": ids}
(OUT / "selection.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
print("선택:", selected)
print("설정: C=1 / 임계값 0.5 초과 / 개발80으로 재학습 / test20 최종 확인")
print("저장: outputs/selection.json (최종평가 이후 변경하지 않습니다.)")
