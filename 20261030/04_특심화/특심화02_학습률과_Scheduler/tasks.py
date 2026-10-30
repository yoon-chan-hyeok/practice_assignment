"""특심화02: Scheduler 생성과 호출 계약. optimizer의 갱신은 실행기가 담당합니다."""
import math
import torch

def make_scheduler(optimizer,kind,epochs):
    # [요구 X02-1] kind=plateau/cosine, epochs는 bool 아닌 양의 int.
    # plateau: mode=min,factor=.5,patience=2,threshold=.001,threshold_mode=abs.
    # cosine: T_max=epochs,eta_min=1e-5. 초기 lr은 optimizer에서 읽는다.
    # 객체만 반환. step/optimizer 재생성 금지. 잘못된 kind/epochs는 ValueError.
    # >>> X02-1
    # TODO X02-1: 위 요구사항을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X02-1")
    # <<< X02-1

def advance_scheduler(scheduler,valid_loss):
    # [요구 X02-2] 한 epoch의 optimizer 갱신과 valid 평가가 이미 끝난 시점에 호출한다.
    # 반환 dict: lr_used와 lr_next는 모든 param group의 lr list.
    # Plateau.step(valid_loss), Cosine.step()만 정확히 1회. optimizer.step() 호출 금지.
    # NaN/inf valid_loss와 지원하지 않는 scheduler는 상태 변경 전에 ValueError.
    # lr_used=이번 epoch 값, lr_next=다음 epoch 값이다. 스케줄러를 평가 전에 호출하지 않는다.
    # >>> X02-2
    # TODO X02-2: 위 요구사항을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X02-2")
    # <<< X02-2
