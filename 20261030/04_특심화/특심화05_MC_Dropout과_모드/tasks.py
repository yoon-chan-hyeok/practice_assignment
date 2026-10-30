"""특심화05: Dropout만 켠 진단과 호출자 상태 보존. BN 통계를 학습시키지 않습니다."""
from contextlib import contextmanager
import torch
from torch import nn

@contextmanager
def dropout_only(model,seed=123):
    # [요구 X05-1] contextmanager. 모델 전체 eval, nn.Dropout만 train. BN은 eval 유지.
    # 각 하위 모듈 원래 training flag·CPU/CUDA RNG를 보존, 예외에도 finally 복구.
    # seed는 bool 아닌 0이상 int. context 내부에만 적용. weight/grad/buffer 변경 금지.
    # 모든 모듈을 하나의 train(flag)로 되돌리면 혼합 모드를 잃으므로 금지.
    # >>> X05-1
    # TODO X05-1: 위 요구사항을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X05-1")
    # <<< X05-1

def mc_predict(model,X,repeats=30,seed=123):
    # [요구 X05-2] 정상 X=(N,F), N>0. repeats는 bool 아닌 int>=2. 빈 입력은 ValueError.
    # X05-1의 context와 no_grad 안에서 softmax 확률(R,N,C)을 수집한다.
    # 반환 mean,variance는 CPU detach(N,C), variance는 unbiased=False.
    # 평균 logits에 softmax 금지. backward/zero_grad/step 금지. 같은 seed 재실행 값 일치.
    # p=0이면 variance≈0. 분산은 불확실성 탐색용이며 보정된 위험도나 신뢰구간이 아니다.
    # >>> X05-2
    # TODO X05-2: 위 요구사항을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X05-2")
    # <<< X05-2
