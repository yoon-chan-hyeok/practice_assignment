"""특심화01: 논리적 NCHW와 물리적 메모리 형식을 구분하고 출력·gradient 동등성을 확인한다."""
import copy
import torch
from support import preserve_rng

def channels_last_copy(x):
    # [요구 X01-1] 입력: 비어 있지 않은 4차원 floating Tensor[N,C,H,W]. 장치는 유지한다.
    # 출력: shape/value/dtype/device를 보존한 독립 storage의 channels_last Tensor.
    # x.permute로 NHWC shape를 만드는 것은 오답. 원본 값/stride/requires_grad 변경 금지.
    # 미분 가능한 입력이면 gradient 경로는 연결되어야 한다(detach 금지).
    # 원본이 이미 channels_last여도 별도 저장공간이어야 한다.
    # 비Tensor/차원 오류/빈 입력/정수 dtype은 ValueError. 값은 atol=0으로 일치.
    # >>> X01-1
    # TODO X01-1: 바로 위의 입력·출력·보존·실패 조건을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X01-1")
    # <<< X01-1

def compare_layouts(model,x):
    # [요구 X01-2] 지원 범위: 입력과 같은 장치·dtype의 Conv/ReLU/Pool/Linear 기반 모델.
    # 동일 가중치를 깊은 복사한 두 모델을 eval로 두고 각각 contiguous/channels_last로 실행.
    # 두 출력의 squared mean을 backward하여 입력 gradient 및 이름별 parameter gradient를 비교.
    # 반환: output_max_abs, input_grad_max_abs, parameter_grad_max_abs의 float dict.
    # 원본 모델·입력·기존 grad·train/eval·전역 난수 상태를 바꾸지 않는다.
    # 파라미터가 없는 모델도 허용하며 parameter 차이는 0.0. 사용 안 된 parameter grad는 양쪽 None.
    # float32 CPU 허용오차 1e-5. 성능 측정이 아니며 '항상 빠름'을 주장하지 않는다.
    # >>> X01-2
    # TODO X01-2: 바로 위의 입력·출력·보존·실패 조건을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X01-2")
    # <<< X01-2
