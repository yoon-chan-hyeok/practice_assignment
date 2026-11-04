import math
import cv2
import numpy as np

def pareto_indices(rows,quality_key="mse",time_key="median_ms"):
    # >>> TODO X04
    # 요구사항 X04 — 두 최소화 비용의 비지배 후보를 찾습니다.
    # rows는 dict 목록이며 quality_key(기본 mse), time_key(기본 median_ms)를 가집니다.
    # A가 B보다 두 값 모두 작거나 같고 하나 이상 엄격히 작을 때만 A가 B를 지배합니다.
    # 반환은 원래 순서의 index 목록. 완전히 같은 비용의 중복 행은 모두 보존합니다.
    # 빈 입력은 []. 음수·NaN·inf 비용은 ValueError. 입력 rows를 정렬하거나 수정하지 마세요.
    # 품질 값은 같은 clean 기준 영상과 비교한 float MSE입니다. Edge 수를 최소화 비용으로 쓰지 않습니다.
    # 측정 시간은 변동하므로 실제 Pareto 목록이 환경마다 같다고 주장하지 않습니다.
    # 테스트에서는 고정 비용으로 지배·동점·오류 규칙만 정확하게 확인합니다.
    raise NotImplementedError("TODO X04: 요구사항을 구현하세요")
    # <<< TODO X04

def mask_metrics(mask,reference):
    # >>> TODO X05
    # 요구사항 X05 — 알려진 정답 마스크가 있는 합성 자료의 품질.
    # mask/reference: 같은 H×W, uint8, 값0/255만. 크기0·shape 불일치·다른 값은 오류입니다.
    # dtype 오류는 TypeError, 나머지 계약 오류는 ValueError로 구분하세요.
    # 흰255를 전경으로 삼아 IoU=교집합/합집합. 둘 다 빈 전경이면 IoU=1.0으로 정의합니다.
    # 8-연결요소를 계산하고 배경 label0을 개수·면적에서 제외합니다.
    # 반환: iou,foreground_pixels,components,정렬된 component_areas.
    # 원본 배열 변경 금지. 성분 라벨 번호의 순서에 의존하지 마세요.
    # 연결요소 수는 진단치이며 적을수록 좋은 점수가 아닙니다. 임계값·커널 탐색 근거에 IoU와 함께 기록합니다.
    raise NotImplementedError("TODO X05: 요구사항을 구현하세요")
    # <<< TODO X05
