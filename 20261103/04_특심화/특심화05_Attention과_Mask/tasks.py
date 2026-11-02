"""이번 교시에서 수정할 구현 파일. 함수별 계약을 읽고 BEGIN/END 구간만 완성한다."""
from copy import deepcopy
from time import perf_counter
import math, random
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

def masked_attention(attention, x, padding_mask, causal=False):
    # TODO X05-1
    # nn.MultiheadAttention(batch_first=True,dropout=0)과 x[B,T,E], mask[B,T] bool True=우측 Padding.
    # 각 행에 1개 이상 실제 위치가 있어야 한다. 미래 key는 causal=True일 때 [T,T] 상삼각 bool Mask로 제외.
    # 반환: output[B,T,E], pooled[B,E], weights[B,heads,T,T]. output/pooled는 gradient 유지.
    # key_mask가 padded query 출력을 0으로 만들지는 않으므로 pooled 계산에서 실제 query만 포함한다.
    # weights는 보고용 detach().clone(); 원본·모듈 모드를 바꾸지 않는다. 실패 시 조용히 NaN을 0으로 덮지 않는다.
    # shape·모든key차단·중간 Padding 위반은 ValueError, bool아닌 mask는 TypeError.
    # BEGIN X05-1
    raise NotImplementedError('X05-1 요구사항을 구현하세요.')
    # END X05-1

def head_statistics(weights, padding_mask):
    # TODO X05-2
    # weights[B,H,T,T]는 dropout=0의 head별 Attention, mask[B,T] bool True=Padding.
    # 각 head에서 유효 query의 entropy(-sum p log p) 평균과 최대 행합 오차를 Python 숫자로 반환한다.
    # 0*log(0)은 0으로 처리한다. Padding key의 확률은 0, 유효 query의 행합은1이어야 한다.
    # 반환: list[dict(head,queries,mean_entropy,max_row_sum_error)]. shape·값범위·확률규칙 위반은 ValueError.
    # weights를 원본 변경하거나 gradient graph와 함께 보고서에 보관하지 않는다. 엔트로피를 설명의 정확도로 부르지 않는다.
    # BEGIN X05-2
    raise NotImplementedError('X05-2 요구사항을 구현하세요.')
    # END X05-2
