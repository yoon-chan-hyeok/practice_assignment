"""특심화07: 조기 종료의 상태와 최적 모델 복원을 분리합니다."""
import copy,math
import torch
from torch import nn

class EarlyStop:
    """mode=min만 지원하는 상태 객체. 상태 저장 메서드는 제공합니다."""
    def __init__(self,patience=8,min_delta=.001):
        if type(patience) is not int or patience<1 or not math.isfinite(min_delta) or min_delta<0: raise ValueError('설정 오류')
        self.patience=patience;self.min_delta=min_delta
        self.best_loss=float('inf');self.best_epoch=0;self.best_state=None
        self.reference=float('inf');self.bad=0;self.last_epoch=0
    def update(self,loss,epoch,model):
        # [요구 X07-1] 유한 loss와 직전보다 큰 양의 정수 epoch. 실패 시 어떤 상태도 변경하지 않는다.
        # 관측 최소 loss(엄격<)마다 deepcopy(state_dict), best_epoch 저장. min_delta와 별개.
        # loss<reference-min_delta일 때만 reference=loss,bad=0. 나머지는 bad+=1.
        # bad>=patience면 True. 매 호출 last_epoch 기록. 동률 모델은 앞 epoch 유지.
        # [1,.8,.79,.78], delta=.05, patience2 -> 4회에 정지, best=.78/epoch4.
        # >>> X07-1
        # TODO X07-1: 위 요구사항을 만족하도록 구현하세요.
        raise NotImplementedError("TODO X07-1")
        # <<< X07-1
    def state_dict(self): return copy.deepcopy(self.__dict__)
    def load_state_dict(self,state): self.__dict__.update(copy.deepcopy(state))

def evaluate_batches(model,batches):
    # [요구 X07-2] 같은 device의 정상 (X,y) 배치 iterable. loss는 CE(sum)/전체 N, 정확도는 정답수/N.
    # 마지막 작은 batch 포함. 빈 전체 또는 0건 batch는 ValueError. 반환 loss,accuracy,samples.
    # eval+no_grad; 모든 하위 모드 복구. forward 실패에도 복구. 기존 grad·BN 통계 보존.
    # backward/step/zero_grad 호출 금지. 입력 iterable을 재순회하지 않는다.
    # >>> X07-2
    # TODO X07-2: 위 요구사항을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X07-2")
    # <<< X07-2

def restore_best(model,stopper):
    # [요구 X07-3] stopper에 best_state가 있어야 한다. 없으면 ValueError(모델 불변).
    # load_state_dict로 buffer까지 복원한다. 모델 모드는 바꾸지 않는다. best_epoch·best_loss 반환.
    # 모델을 이후 변경해도 stopper.best_state가 변하지 않아야 한다. optimizer 재개용 기능이 아니다.
    # >>> X07-3
    # TODO X07-3: 위 요구사항을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X07-3")
    # <<< X07-3
