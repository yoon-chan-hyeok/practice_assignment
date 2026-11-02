"""이번 교시에서 수정할 구현 파일. 함수별 계약을 읽고 BEGIN/END 구간만 완성한다."""
from copy import deepcopy
from time import perf_counter
import math, random
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

def trace_lstm(cell, x, h0=None, c0=None):
    # TODO X03-1
    # cell은 bias=True nn.LSTMCell. x[B,T,F], 선택 h0/c0[B,H]. 반환은 output,h,c,gate_log.
    # gate 순서는 PyTorch의 i,f,g,o이다. cell의 두 linear 결과를 더한 뒤 4등분한다.
    # i/f/o=sigmoid, g=tanh, c=f*c+i*g, h=o*tanh(c). output·h·c는 미분 경로를 유지한다.
    # gate_log는 dict i/f/g/o[B,T,H]이며 보고용이므로 detach().clone()한다.
    # 빈 입력은 ValueError. 같은 가중치의 nn.LSTM과 출력·상태·gradient가 일치해야 한다.
    # Gate 값은 모델의 상태 관찰이지 인간의 기억·망각 원인을 증명하는 근거가 아니다.
    # BEGIN X03-1
    raise NotImplementedError('X03-1 요구사항을 구현하세요.')
    # END X03-1

def summarize_gates(gate_log, lengths):
    # TODO X03-2
    # gate_log 각 값은 [B,T,H], lengths는 실제 길이[B]. 원본을 바꾸지 않는다.
    # Padding 시점은 제외하고 gate별 실제 원소 수·평균·최솟값·최댓값을 반환한다.
    # 반환: i,f,g,o 순서의 list[dict(gate,count,mean,min,max)]. Python 숫자만 포함한다.
    # 필수 키·shape 불일치, 0길이, 유효 위치의 비유한 값은 ValueError.
    # 분모는 실제 시점 수×H이다. 표본별 평균의 단순 평균과 혼동하지 않는다.
    # BEGIN X03-2
    raise NotImplementedError('X03-2 요구사항을 구현하세요.')
    # END X03-2
