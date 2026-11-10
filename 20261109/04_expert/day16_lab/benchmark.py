"""측정 범위가 다른 실행이나 mock 값을 실제 성능 회귀로 비교하지 않습니다."""
import math
import numpy as np


def compare_latency(baseline,candidate,tolerance=0.20):
    # S10 요구사항
    # keys backend/model_digest/device/precision/input_shape/scope는 같아야 하며 None 불가.
    # backend=mock, 기록 재생, DESGIN_ONLY는 실제 추론 성능 비교 대상 아님.
    # timings_ms는 3개 이상 유한한 양수; count/warmup을 임의로 섞지 않는다.
    # p50·p95를 각각 구하고 candidate_p95 > baseline_p95*(1+tolerance)면 regression=True.
    # tolerance finite 0이상; 등호는 회귀 아님. 입력 불변. 단위 ms.
    # 환경 차이/샘플 부족은 ValueError로 거부. CPU 측정에 GPU VRAM=0을 꾸며 넣지 않는다.
# TODO S10
    raise NotImplementedError('S10: comparable timing policy')
# TODO 끝 S10
