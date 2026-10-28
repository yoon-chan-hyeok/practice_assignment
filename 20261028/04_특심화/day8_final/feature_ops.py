"""실습04에서 완성한 행별 특성 변환. 이 모듈은 모델 복원 시에도 필요합니다."""
import numpy as np
from data_io import check_features

def add_features(X):
    """[D8-P01] 원본4열을 유지하고 두 파생 열을 추가한 새 DataFrame을 반환합니다.
    log_input_chars = log1p(input_chars)
    chars_per_slot = input_chars / (1 + allowed_tools)
    NaN, 인덱스와 행 순서를 유지합니다. y나 다른 행의 통계는 사용하지 않습니다.
    """
    # TODO D8-P01: 함수의 계약과 README를 보고 구현하세요.
    raise NotImplementedError("TODO D8-P01")
