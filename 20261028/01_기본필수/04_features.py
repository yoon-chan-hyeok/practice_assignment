"""실습 04: 다른 행의 통계나 정답을 사용하지 않는 파생 열 하나를 만듭니다."""
from pathlib import Path
import pandas as pd
import numpy as np
raw = pd.read_csv(Path(__file__).resolve().parent / "requests.csv")
# 원본 파일은 덮어쓰지 않습니다. 글자 수만 복사하고 정답·실행시간은 선택하지 않습니다.
features = raw[["input_chars"]].copy()
# TODO B04: np.log1p로 글자 수의 로그 변환 열을 추가하세요. 각 행의 값만 사용합니다.
features["log_input_chars"] = 0.0
# TODO 끝
print(features.head().round(3).to_string(index=False))
print("행/열:", features.shape)
print("원본 열:", raw.columns.tolist())
