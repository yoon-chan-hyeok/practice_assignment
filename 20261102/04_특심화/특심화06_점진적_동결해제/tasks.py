"""특심화06: ResNet18 Head -> layer4+Head 전환과 BN 동결 정책을 분리해 검증한다."""
import torch
from torch import nn

def configure_transfer(model,stage,optimizer=None):
    # [요구 X06-1] model: 새 fc를 단 ResNet18. stage=head/partial. 단계 역전환은 ValueError.
    # head=fc만 학습. partial=layer4+fc, 단 모든 BatchNorm의 affine·running statistics는 고정.
    # lr_head=1e-3/lr_layer4=1e-4, AdamW weight_decay=1e-4. 각 parameter 그룹에 정확히 1회.
    # 기존 optimizer가 오면 같은 객체를 반환하고 fc의 moment/step은 보존. 새 layer4만 add_param_group.
    # same-stage 재호출은 중복 추가하지 않는 idempotent 동작. 고정 parameter의 기존 grad는 None으로 제거.
    # model.eval 후 학습할 영역만 train; 그 뒤 모든 BN을 다시 eval. 학습 매 epoch마다 이 정책 재적용.
    # 반환 optimizer. 원본 weight를 초기화하거나 seed 변경 금지. 구조검사(weights=None)는 전이 성능이 아니다.
    # >>> X06-1
    # TODO X06-1: 바로 위의 입력·출력·보존·실패 조건을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X06-1")
    # <<< X06-1

def trainable_report(model,optimizer):
    # [요구 X06-2] named parameter마다 name/shape/numel/trainable/group/lr를 Python 값으로 반환.
    # trainable parameter 집합과 optimizer 그룹 집합이 정확히 같아야 한다.
    # 중복 parameter/외부 parameter/누락 parameter/동결 parameter 포함은 ValueError.
    # 모든 BN eval·affine False인지 검사. 검사는 상태를 변경하지 않는다.
    # report 합계로 Head=1026, partial은 BN affine 제외 결과를 확인한다. 수치를 하드코딩하지 않는다.
    # >>> X06-2
    # TODO X06-2: 바로 위의 입력·출력·보존·실패 조건을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X06-2")
    # <<< X06-2
