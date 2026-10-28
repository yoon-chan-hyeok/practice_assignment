"""실습 08: 직접 생성한 저장 모델을 새 프로세스에서 복원합니다. 학습·후보 선택은 하지 않습니다."""
from pathlib import Path
import json
import pandas as pd
import numpy as np
import joblib
# features.py의 이름 있는 함수가 저장된 모델에서 참조됩니다. 프로젝트 파일을 함께 보존하세요.
HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"
plan = json.loads((OUT / "selection.json").read_text(encoding="utf-8"))
raw = pd.read_csv(HERE / "data/requests.csv").set_index("request_id")
expected = pd.read_csv(OUT / "test_predictions.csv")
# 신뢰할 수 없는 파일을 읽지 않습니다. main.py가 직접 저장한 파일에만 이 예제를 사용하세요.
model = joblib.load(OUT / "pipeline.joblib")
X = raw.loc[expected["request_id"], plan["features"]]
positive_column = model.classes_.tolist().index(1)
# TODO H08: 복원 모델로 같은 ID 순서의 실패 확률을 구하세요. fit은 호출하지 않습니다.
probability = np.zeros(len(X))
# TODO 끝
prediction = (probability > plan["threshold"]).astype(int)
print("ID 순서 동일:", X.index.tolist() == expected["request_id"].tolist())
print("확률 동일:", np.allclose(probability, expected["probability_failed"], rtol=1e-10, atol=1e-12))
print("예측 동일:", np.array_equal(prediction, expected["predicted"]))
print("복원은 고정 버전의 재현입니다. 점수를 보고 임계값을 다시 고르지 않습니다.")
