
"""
실습 06: AI 모델의 ONNX·TensorRT 배포 파이프라인 설계

[실습 목적]
AI 모델을 개발한 이후 실제 서비스 환경에 배포하기까지의
과정을 이해하고, 배포 파이프라인을 단계별로 설계합니다.

[주요 동작]
1. 모델 배포에 필요한 처리 단계를 정의합니다.
2. 각 단계를 올바른 순서로 stages 리스트에 작성합니다.
3. 배포 설계 정보를 JSON 파일로 저장합니다.

[주의사항]
- 실제 ONNX 변환이나 TensorRT 최적화를 수행하지 않습니다.
- 실제 하드웨어에서 추론 성능을 측정하지 않습니다.
- Tesseract OCR 자체를 ONNX로 변환하는 실습이 아닙니다.
- 배포 과정의 설계만 기록하는 DESIGN_ONLY 실습입니다.
"""

from pathlib import Path
import json

base = Path(__file__).resolve().parent

# ============================================================
# TODO B07: AI 모델 배포 파이프라인 단계 정의
# ============================================================
#
# [요구사항]
# 1. AI 모델을 실제 서비스 환경에 배포하기 위한
#    주요 처리 단계를 순서대로 정의하세요.
#
# 2. 다음 과정을 참고하여 배포 흐름을 구성하세요.
#
#    ① 모델 준비
#       - 학습 완료된 AI 모델과 입력·출력 규격 확인
#
#    ② ONNX 변환(Export)
#       - ONNX 변환을 지원하는 모델을 ONNX 형식으로 변환
#
#    ③ ONNX 검증
#       - ONNX Runtime 등으로 원본 모델과 출력 결과 비교
#
#    ④ TensorRT 최적화
#       - 대상 NVIDIA GPU 환경에 맞게 추론 엔진 생성
#
#    ⑤ 하드웨어 배포
#       - Jetson 또는 NVIDIA GPU 장비에 모델 배포
#
#    ⑥ 추론 성능 검증
#       - 지연시간(Latency), 정확도, 메모리 사용량 등 측정
#
# 3. 각 단계의 이름을 문자열(str)로 작성하고,
#    stages 리스트에 실행 순서대로 저장하세요.
#
# [작성 예시]
# stages = ["모델 준비", "ONNX 변환", ...]
#
# [주의사항]
# - 실제 모델 변환이나 추론을 실행하는 코드를 작성하지 않습니다.
# - 배포 흐름을 문자열 리스트로 표현하는 것이 목표입니다.
# - 설계만 수행하므로 status는 "DESIGN_ONLY"로 유지합니다.
# - 측정하지 않은 성능값이나 하드웨어 정보를 임의로 입력하지 않습니다.
# ============================================================

stages = []  # TODO: 배포 단계들을 순서대로 작성하세요.

# TODO 끝 B07

# 설계 정보 저장 (실제 실행 결과가 아님)
plan = {
    'stages': stages,
    'status': 'DESIGN_ONLY',
    'target_device': None,
    'tensorrt_version': None,
    'engine_sha256': None,
    'latency_ms': None,
    'checked_on_hardware': False
}

# 배포 설계 결과를 JSON 파일로 저장
(base / 'p06_deployment_plan.json').write_text(
    json.dumps(plan, ensure_ascii=False, indent=2),
    encoding='utf-8'
)

# 배포 단계를 순서대로 출력
print(' -> '.join(stages))

print(
    'DESIGN_ONLY: 오늘은 설계 기록. '
    'Tesseract 자체를 ONNX로 변환하는 예제가 아닙니다.'
)
