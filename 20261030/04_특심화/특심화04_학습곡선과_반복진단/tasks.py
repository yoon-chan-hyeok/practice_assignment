"""특심화04: 개별 seed의 best와 평균 곡선의 최저점을 구분합니다."""
import numpy as np
import pandas as pd

def summarize_best(history):
    # [요구 X04-1] DataFrame(seed,epoch,train_loss_eval,valid_loss). 최소2 seed, 같은 epoch 집합.
    # 각 seed의 epoch는 1부터 연속, seed+epoch 중복 없음, loss는 유한. 아니면 ValueError.
    # 반환: seed,best_epoch,best_valid_loss,train_loss_at_best,gap_at_best,last_valid_loss.
    # best는 valid 최소, 동률이면 작은 epoch. gap=valid-train(동일 epoch의 eval 측정).
    # 원본/행순서 변경 금지. seed 오름차순 결과. 테스트 데이터는 입력에 포함하지 않는다.
    # >>> X04-1
    # TODO X04-1: 위 요구사항을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X04-1")
    # <<< X04-1

def summarize_curve(history):
    # [요구 X04-2] X04-1과 같은 입력, 같은 검사를 적용한다.
    # 반환 epoch별 train_mean,train_std,valid_mean,valid_std,n. std는 표본표준편차 ddof=1.
    # 개별 best만 골라 평균 내지 않는다. 모든 seed의 같은 epoch를 비교한다.
    # 결과를 신뢰구간이라고 부르지 않는다. 각 seed best_epoch와 평균 곡선 best_epoch는 다를 수 있다.
    # >>> X04-2
    # TODO X04-2: 위 요구사항을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X04-2")
    # <<< X04-2
