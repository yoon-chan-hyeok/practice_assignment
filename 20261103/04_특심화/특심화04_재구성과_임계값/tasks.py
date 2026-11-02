"""이번 교시에서 수정할 구현 파일. 함수별 계약을 읽고 BEGIN/END 구간만 완성한다."""
from copy import deepcopy
from time import perf_counter
import math, random
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

def masked_mse(prediction, target, padding_mask):
    # TODO X04-1
    # prediction,target[B,T,F] 동일 실수 dtype/device, mask[B,T] bool True=제외.
    # 유효한 원소만 선택하여 제곱오차 합/유효 원소 수를 scalar Tensor로 반환한다.
    # Padding에 NaN이 있어도 제외 위치는 loss에 포함하지 않는다. 곱셈으로 NaN*0을 만들지 않는다.
    # 출력은 prediction으로 gradient가 흐르고 제외 위치 gradient는 0이다. 원본 변경 금지.
    # 빈 입력·전체 Padding·유효 원소의 NaN/inf·shape 위반은 ValueError, mask dtype 오류는 TypeError.
    # 완료: 길이별 평균의 단순 평균이 아닌 실제 시점 수×특성 수의 가중 평균이다.
    # BEGIN X04-1
    raise NotImplementedError('X04-1 요구사항을 구현하세요.')
    # END X04-1

def choose_threshold(errors, labels):
    # TODO X04-2
    # errors는 valid의 1차원 유한 비음수 재구성 오류, labels는 같은 길이 0/1이며 두 클래스 모두 존재.
    # 후보는 고유 오류의 인접 중점과 양 끝 바깥 값. error > threshold일 때만 이상1로 예측한다.
    # 주 지표는 F1; 분모0이면0. 동점은 더 큰 threshold를 선택한다. 후보표와 best dict를 반환한다.
    # test는 이 함수의 인자가 아니며 후보 생성·지표 선택에도 사용하지 않는다.
    # 반환 필드는 threshold,f1,tp,fp,fn. 정상 train으로 AE를 학습한 뒤 valid에서만 이 함수를 호출한다.
    # 선택 확장 명령은 계획·모델을 저장한 다음 별도 test를 1회 읽는다. 결과를 본 뒤 다시 선택하지 않는다.
    # BEGIN X04-2
    raise NotImplementedError('X04-2 요구사항을 구현하세요.')
    # END X04-2
