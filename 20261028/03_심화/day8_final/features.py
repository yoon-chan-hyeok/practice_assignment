"""제공 모듈: 실습04의 행별 공식을 재사용합니다. 모델을 복원할 때도 이 파일이 필요합니다."""
import numpy as np

def add_features(X):
    """자기 행의 수치만으로 두 열을 추가합니다. 원본·인덱스·행 순서는 보존합니다."""
    out = X.copy()
    out["log_input_chars"] = np.log1p(out["input_chars"])
    out["chars_per_slot"] = out["input_chars"] / (1.0 + out["allowed_tools"])
    return out
