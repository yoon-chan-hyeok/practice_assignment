"""특심화01: Optimizer 비교를 하나의 seed 점수가 아니라 대응 실험으로 만든다."""
import math
import torch
import pandas as pd

def make_optimizer(parameters, kind, lr, weight_decay=0.0):
    # [요구 X01-1] 필수: Parameter iterable, kind('sgd'/'adamw'), lr>0. 선택: weight_decay>=0.
    # 반환: 새 Optimizer. SGD momentum=0.9, AdamW betas=(0.9,0.999). 두 후보 모두 전달 WD 명시.
    # parameters는 generator일 수 있다. 한 번만 읽고 requires_grad=True인 것만 사용한다.
    # 빈 학습 목록, 지원하지 않는 종류, 비유한/0이하 lr, 음수/비유한 WD는 ValueError.
    # 생성만 수행한다. 모델 초기화·seed 변경·zero_grad·step·parameter 변경 금지.
    # 반환 객체 param_groups의 parameter가 원래 Parameter 객체인지 검사한다.
    # >>> X01-1
    # TODO X01-1: 위 요구사항을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X01-1")
    # <<< X01-1

def summarize_runs(rows):
    # [요구 X01-2] rows: setting(str), seed(int), best_valid_loss(유한 float)를 가진 dict 목록.
    # 설정별 n·mean·std(ddof=1)를 반환. setting 오름차순, 각 설정 동일 seed 집합(최소2개).
    # 중복 setting+seed/비어 있음/비유한 loss/짝이 안 맞는 seed 집합은 ValueError.
    # 원본 수정 금지. 평균 순위만으로 통계적 우열·실제 서비스 성능을 주장하지 않는다.
    # >>> X01-2
    # TODO X01-2: 위 요구사항을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X01-2")
    # <<< X01-2
