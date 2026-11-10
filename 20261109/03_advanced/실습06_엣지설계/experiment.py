
"""
실습 06: Jetson·DeepStream 기반 AI 추론 시스템 배포 설계

[실습 목적]
NVIDIA Jetson 환경에서 DeepStream 기반 영상 처리 시스템을
배포할 때 필요한 파이프라인과 성능 평가 항목을 설계합니다.

[주요 동작]
1. DeepStream 영상 처리 파이프라인 확인
2. 추론 성능을 평가하기 위한 측정 지표 정의
3. Warm-up 및 반복 측정 조건 확인
4. 배포 설계 정보를 JSON 파일로 저장

[주의사항]
- 실제 Jetson 장비나 DeepStream을 실행하지 않습니다.
- 측정하지 않은 성능 수치를 임의로 작성하지 않습니다.
- 이번 실습은 설계만 수행하는 DESIGN_ONLY 단계입니다.
"""

from pathlib import Path
import sys
import json
import cv2
import numpy as np
import pandas as pd

base = Path(__file__).resolve().parent
root = base.parent
data = root / 'data'
out = base / 'outputs'
out.mkdir(exist_ok=True)

sys.path.insert(0, str(root / 'day16_documents'))

from fields import extract, extract_items, validate, reconcile
from evaluate import cer

lesson = json.loads(
    (data / 'lesson.json').read_text(encoding='utf-8')
)

# ============================================================
# 1. Jetson·DeepStream 배포 파이프라인 설정
# ============================================================

plan = {
    'status': 'DESIGN_ONLY',

    # 영상 디코딩 → 다중 스트림 처리 → AI 추론
    # → 선택적 객체 추적 → 결과 시각화 → 출력
    'pipeline': [
        'decode',
        'nvstreammux',
        'nvinfer',
        'optional nvtracker',
        'nvdsosd',
        'sink'
    ],

    # 실제 장비 및 소프트웨어 버전은 아직 확인하지 않음
    'target_device': None,
    'jetpack': None,
    'tensorrt': None,
    'deepstream': None,

    # 성능 측정 전 30프레임을 준비 과정으로 사용
    'warmup_frames': 30,

    # 성능 측정에 사용할 프레임 수
    'measure_frames': 300,

    # 측정 결과의 안정성을 확인하기 위해 3회 반복
    'runs': 3,

    # 영상 디코딩을 포함한 전체 처리 구간 측정
    'include_decode': True,

    # 입력 영상 크기: 640×480
    'input_size': [640, 480],

    # FPS 제한 조건은 아직 지정하지 않음
    'fps_limit': None
}


# ============================================================
# TODO C06: AI 추론 시스템 성능 측정 항목 정의
# ============================================================
#
# [요구사항]
#
# 1. Jetson·DeepStream 시스템을 실제 하드웨어에 배포했을 때
#    측정해야 할 주요 성능 지표를 정의하세요.
#
# 2. 다음 항목들을 참고하여 측정 지표를 선정하세요.
#
#    ① 추론 지연시간(Latency)
#       - 영상 입력부터 처리 결과가 출력되기까지 걸리는 시간
#       - 단위: ms(밀리초)
#       - 평균 지연시간과 P95 지연시간 등을 고려
#
#    ② 처리 속도(Throughput)
#       - 시스템이 1초 동안 처리하는 프레임 수
#       - 단위: FPS(Frames Per Second)
#
#    ③ CPU 사용률
#       - 영상 처리 중 CPU 자원 사용 비율
#       - 단위: %
#
#    ④ GPU 사용률
#       - AI 추론 및 영상 처리 중 GPU 사용 비율
#       - 단위: %
#
#    ⑤ 메모리 사용량
#       - 시스템 실행 중 사용하는 메모리 용량
#       - 단위: MB
#       - Jetson은 CPU와 GPU가 메모리를 공유하므로
#         일반적인 독립형 GPU의 VRAM과 구분해야 함
#
#    ⑥ 소비 전력(Power Consumption)
#       - 추론 시스템이 동작할 때 소비하는 전력
#       - 단위: W(와트)
#
#    ⑦ 장치 온도(Temperature)
#       - 장시간 추론 시 장치의 발열 상태
#       - 단위: °C
#
# 3. 선정한 측정 항목의 이름을 문자열(str)로 작성하여
#    measurements 리스트에 저장하세요.
#
# 4. 다음 형식으로 작성하세요.
#
#    plan['measurements'] = [
#        '측정항목_1',
#        '측정항목_2',
#        '측정항목_3'
#    ]
#
# 5. 측정 항목의 이름은 영문 snake_case로 작성하고,
#    가능한 경우 단위를 이름에 포함하세요.
#    예: throughput_fps, power_w
#
# [측정 조건]
# - Warm-up: 30 Frames (성능 집계에서 제외)
# - Measurement: 300 Frames
# - Runs: 3회 반복 측정
# - Input Resolution: 640×480
# - Decode 포함: True
#
# [주의사항]
# - 실제 성능 측정 코드는 구현하지 않습니다.
# - 측정 항목 이름만 정의합니다.
# - 측정하지 않은 지연시간, FPS, 전력 등을 생성하지 않습니다.
# - 실제 Jetson 장비가 없으므로 하드웨어 검증 상태는 False입니다.
# - nvinfer만 연결한다고 OCR/VLM이 자동으로 구현되는 것은 아닙니다.
#
# [기대 결과]
# measurements에 작성한 항목들이
# deployment_plan.json의 measurements에 저장되고,
# results에는 해당 항목들이 None으로 초기화되어야 합니다.
# ============================================================

plan['measurements'] = []  # TODO: 성능 측정 항목 작성

# TODO 끝 C06


# ============================================================
# 2. 측정 결과 초기화
# ============================================================

# measurements에 작성한 측정 항목들을 Key로 사용
# 실제 측정하지 않았으므로 모든 결과는 None으로 설정
plan['results'] = {
    name: None for name in plan['measurements']
}

# 배포 설계 시 주의사항 기록
plan['note'] = (
    'Jetson 공유 메모리를 dGPU 전용 VRAM과 같다고 해석하지 않는다. '
    'nvinfer만 연결해 임의 OCR/VLM을 자동 지원한다고 주장하지 않는다.'
)


# ============================================================
# 3. 배포 설계 JSON 저장 및 출력
# ============================================================

# 배포 설계 정보 저장 (실제 하드웨어 측정 결과가 아님)
(out / 'deployment_plan.json').write_text(
    json.dumps(plan, ensure_ascii=False, indent=2),
    encoding='utf-8'
)

# 영상 처리 파이프라인 출력
print(' -> '.join(plan['pipeline']))

# 정의한 성능 측정 항목 개수 출력
print(
    '측정 항목:', len(plan['measurements']),
    '하드웨어 실행: 미수행'
)
