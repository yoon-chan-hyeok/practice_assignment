"""특심화06: 통계 정규화와 파라미터 감쇠를 구분해 검증합니다."""
import math
import torch
from torch import nn
import pandas as pd
def normalization_probe(activation):
    # [입력] activation(N,C), N>=32이며 유한한 float32 Tensor. train 입력만 사용합니다.
    # [실험] batch_size=2,8,32 각각 5개 순열 seed로 동일 activation을 순회합니다. 가중치 갱신은 없습니다.
    # BN은 momentum=0.1, affine=False, LayerNorm은 elementwise_affine=False로 새로 만듭니다.
    # [측정] BN의 최종 running_mean과 전체 train 평균의 MSE, batch별 입력 평균의 분산 평균을 기록합니다.
    # LayerNorm에는 running 통계가 없으므로 running_mean_mse=None을 기록합니다. 샘플별 정규화 출력의 평균 절댓값도 기록합니다.
    # [출력] norm,batch_size,seed,batches,seen,batch_mean_variance,running_mean_mse,output_mean_abs의 DataFrame.
    # [조건] shuffle 순서는 norm끼리 동일합니다. 마지막 배치가 1건이면 이 진단에서는 해당 배치를 두 방식 모두 제외하고 seen에 반영합니다.
    # [해석] batch별 평균 분산, BN running 추정 오차, LN 출력 평균은 다른 통계입니다. LN이 반드시 더 좋은 분류기라고 결론내리지 않습니다.
    # [주의] 배치가 작으면 통계 갱신 횟수도 많아집니다. 결과를 batch 크기만의 인과효과로 주장하지 마세요.
    # >>> X06-1
    # TODO X06-1: 위 요구사항을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X06-1")
    # <<< X06-1


def decay_groups(model,weight_decay=.01):
    # [요구 X06-2] Linear·BatchNorm1d·LayerNorm과 parameter 없는 모듈로 구성된 정상 ANN.
    # 학습 가능한 모든 Parameter를 정확히 한 번 포함하는 두 param group을 반환한다.
    # bias와 BatchNorm/LayerNorm의 affine parameter는 weight_decay=0, 나머지 weight는 전달값.
    # 모듈 유형+recurse=False named_parameters를 사용. 이름에 'bn' 포함 여부로 판정 금지.
    # 공유 Parameter는 중복 넣지 않는다. 같은 객체가 여러 경로에 있으면 먼저 방문한 경로 정책 적용.
    # frozen 제외, 원본 requires_grad/값 변경 금지. 비유한/음수 weight_decay는 ValueError.
    # >>> X06-2
    # TODO X06-2: 위 요구사항을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X06-2")
    # <<< X06-2
