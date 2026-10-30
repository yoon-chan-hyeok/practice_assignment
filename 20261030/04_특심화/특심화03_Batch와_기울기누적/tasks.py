"""특심화03: 마지막 작은 묶음을 버리지 않는 정확한 gradient accumulation."""
import torch
from torch import nn
from torch.nn import functional as F

def group_microbatches(batches,accumulation_steps=4):
    # [요구 X03-1] batches는 (X,y) iterable, accumulation_steps는 bool 아닌 양의 int.
    # 원래 순서로 최대 accumulation_steps개씩 묶은 list[list[tuple]]를 반환한다.
    # 마지막 1~3개도 보존. 원본 Tensor 복사/병합/변경 금지. 빈 입력은 빈 list.
    # 예: 9개 micro-batch, steps4 -> 그룹길이 [4,4,1]. 잘못된 steps는 ValueError.
    # >>> X03-1
    # TODO X03-1: 위 요구사항을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X03-1")
    # <<< X03-1

def accumulated_step(model,optimizer,micro_batches):
    # [요구 X03-2] float32/64 X=(n,F), long y=(n,), 같은 장치, 각 n>0인 정상 입력 목록.
    # 빈 목록/빈 micro-batch, BN(모든 모드) 또는 p>0 Dropout 포함 모델은 ValueError.
    # 검사는 zero_grad 전에 수행. 큰 batch와 등가를 논하는 실험이므로 BN/Dropout을 제외한다.
    # 그룹 전체에서 zero_grad 1회→각 CE(sum)/전체 N의 backward→step 1회.
    # 반환: loss(float),samples(int),gradients(list[Tensor|None]); gradient는 step 직전 독립 사본.
    # 기존 gradient를 누적하거나 micro-batch 수만으로 나누거나 매번 step하면 안 된다.
    # 불균등 [17,13]와 마지막 작은 그룹도 처리. float64 큰 batch와 atol1e-10/rtol1e-8 대조.
    # >>> X03-2
    # TODO X03-2: 위 요구사항을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X03-2")
    # <<< X03-2
