"""이번 교시에서 수정할 구현 파일. 함수별 계약을 읽고 BEGIN/END 구간만 완성한다."""
from copy import deepcopy
from time import perf_counter
import math, random
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

def pack_ordered(x, lengths, sort=True):
    # TODO X01-1
    # 입력: x[B,T,F] 실수 Tensor; lengths[B] int64, 각 길이 1..T. 길이 값은 CPU로 보낸다.
    # 길이를 0 값의 위치로 추정하지 않는다. sort=True이면 안정적인 내림차순 정렬로 동률 원순서를 보존한다.
    # 반환: (PackedSequence, undo[B] CPU int64). unpack 뒤 restored[undo]가 원래 표본 순서이다.
    # sort=False는 enforce_sorted=False를 사용하며 unpack 결과가 이미 원순서이므로 undo=arange(B).
    # 원본/장치/dtype/autograd 연결을 보존한다. x나 lengths를 제자리 수정하거나 detach하지 않는다.
    # 실패: 빈 축·길이 범위/형태 위반은 ValueError, 실수가 아닌 x나 비int64 lengths는 TypeError.
    # 완료: 정렬 방식 두 가지의 unpack 값·길이·모델 출력·입력 gradient가 일치해야 한다.
    # BEGIN X01-1
    raise NotImplementedError('X01-1 요구사항을 구현하세요.')
    # END X01-1

def restore_padded(packed, undo, total_length):
    # TODO X01-2
    # 입력: packed는 앞 함수 결과, undo는 0..B-1의 중복 없는 역순열, total_length는 원래 최대 길이.
    # 반환: (padded[B,total_length,H], lengths[B]) 모두 원래 표본 순서. padded의 채움값은 0.
    # 역순열 범위·중복을 검증한다. 길이는 CPU int64. Tensor의 장치·dtype·미분 경로는 보존한다.
    # 잘못된 역순열이나 total_length가 실제 최대 길이보다 작으면 ValueError.
    # 완료: 값뿐 아니라 길이가 원래 순서인지 확인한다. 같은 길이 표본을 바꿔 끼우지 않는다.
    # BEGIN X01-2
    raise NotImplementedError('X01-2 요구사항을 구현하세요.')
    # END X01-2
