"""이번 교시에서 수정할 구현 파일. 함수별 계약을 읽고 BEGIN/END 구간만 완성한다."""
from copy import deepcopy
from time import perf_counter
import math, random
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

def evaluate_batches(model, loader):
    # TODO X06-1
    # loader는 (x,lengths,y,ids), model은 분류 logits[B,C] 반환. 장치는 호출자가 맞춘다.
    # 평가 중 eval+inference_mode 사용. loss는 각 배치 CE mean×실제 표본 수의 합/전체 표본 수.
    # 반환: loss,accuracy,ids,predictions,targets 딕셔너리. ID·예측은 실제 방문 순서를 그대로 유지.
    # 모든 하위모듈의 원래 mode, weights/buffers/기존grad와 CPU·CUDA/Python/NumPy RNG를 복구한다.
    # 성공/예외 모두 복구하며 optimizer 갱신·zero_grad·backward 금지. 빈 loader는 ValueError.
    # 모델에 test loader를 전달하지 않는다. 마지막 작은 배치도 같은 표본 가중 기준으로 계산한다.
    # BEGIN X06-1
    raise NotImplementedError('X06-1 요구사항을 구현하세요.')
    # END X06-1

def check_padding_invariance(model, x, lengths, value=999.0):
    # TODO X06-2
    # 실제 시점은 그대로 두고 우측 Padding만 value로 바꿔 두 번 예측한다.
    # 각 예측을 동일한 eval 상태에서 수행하고 atol=1e-5,rtol=1e-5로 비교한다.
    # 반환: unchanged(bool),max_abs_diff(float),padded_positions(int). 예측값·원본·상태를 수정하지 않는다.
    # model의 weights/buffers/grad·mode·RNG를 성공/실패 모두 보존한다. 길이0·길이>T는 ValueError.
    # 불변이 아니면 False를 보고하며 임의로 예측을 같게 고치지 않는다. 기본 모델은 packed RNN/LSTM 및 masked Transformer이다.
    # BEGIN X06-2
    raise NotImplementedError('X06-2 요구사항을 구현하세요.')
    # END X06-2
