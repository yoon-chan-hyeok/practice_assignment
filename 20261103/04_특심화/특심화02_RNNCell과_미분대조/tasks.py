"""이번 교시에서 수정할 구현 파일. 함수별 계약을 읽고 BEGIN/END 구간만 완성한다."""
from copy import deepcopy
from time import perf_counter
import math, random
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

def copy_rnn_weights(reference, cell):
    # TODO X02-1
    # reference는 1층 단방향 bias=True tanh nn.RNN, cell은 같은 입력/hidden·장치·dtype의 nn.RNNCell.
    # 지원 범위를 검사한 뒤 weight_ih, weight_hh, bias_ih, bias_hh 네 값을 대응시켜 복사한다.
    # 반환은 cell. Parameter를 새 객체로 교체하지 말고 no_grad에서 copy_를 사용한다.
    # 원본 reference와 기존 gradient는 바꾸지 않는다. 지원하지 않는 층·방향·shape·dtype는 ValueError.
    # 완료: 네 가중치 값은 같고, source와 destination의 메모리는 공유되지 않는다.
    # BEGIN X02-1
    raise NotImplementedError('X02-1 요구사항을 구현하세요.')
    # END X02-1

def unroll_rnn(cell, x, h0=None):
    # TODO X02-2
    # x[B,T,F] 실수 Tensor, h0[B,H] 선택(없으면 같은 device/dtype의 0). 출력은 (output[B,T,H], h_last[B,H]).
    # 시간축 순서로 cell(x[:,t],h)를 호출한다. 입력·h0를 수정하지 않고 모든 시점의 gradient를 연결한다.
    # detach, no_grad, 출력에 같은 가변 버퍼 재사용 금지. 빈 시간축은 ValueError.
    # 같은 가중치의 nn.RNN과 output·h_last·x/h0/네 파라미터의 gradient를 대조한다.
    # 허용오차: CPU float64 atol=1e-9 rtol=1e-7; float32 atol=1e-6 rtol=1e-5.
    # BEGIN X02-2
    raise NotImplementedError('X02-2 요구사항을 구현하세요.')
    # END X02-2
