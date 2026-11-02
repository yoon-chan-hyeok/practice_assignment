"""특심화02: 같은 수식으로 일반·Depthwise·Dilated Conv의 shape와 비용을 검증한다."""
import torch
from torch.nn import functional as F

def conv_cost(shape, cout, kernel, stride=1, padding=0, dilation=1, groups=1, bias=True):
    # [요구 X02-1] shape=(N,C,H,W). kernel/stride/padding/dilation은 이 과제에서는 정수만.
    # N/C/H/W/cout/kernel/stride/dilation/groups는 양의 정수, padding은 0 이상.
    # bool을 정수 크기로 받지 않는다. C와 cout는 groups로 나누어떨어져야 한다.
    # Hout=(H+2P-D(K-1)-1)//S+1. W도 동일. 공간이 0이하이면 ValueError.
    # params=cout*(C/groups)*K*K + bias 개수. MACs=N*cout*Hout*Wout*(C/groups)*K*K.
    # bias 덧셈, 활성함수, 데이터 이동은 MAC에서 제외. 1MAC을 곱-누적 1회로 정의한다.
    # 반환 {'shape': tuple, 'parameters': int, 'macs': int}. 실제 속도·VRAM이 아니다.
    # >>> X02-1
    # TODO X02-1: 바로 위의 입력·출력·보존·실패 조건을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X02-1")
    # <<< X02-1

def grouped_reference(x, weight, bias=None, stride=1, padding=0, dilation=1, groups=1):
    # [요구 X02-2] F.conv2d(groups=groups)를 그대로 호출하지 말고 그룹별 일반 Conv로 구현.
    # 입력 x[N,C,H,W], weight[Cout,C/groups,K,K], bias[Cout] 또는 None. square kernel만 지원.
    # 입력/weight/bias를 그룹별로 자르고 groups=1 conv 후 출력 channel(dim=1)로 concat.
    # detach/NumPy 변환 금지: 입력·weight·bias gradient가 연결되어야 한다.
    # 잘못된 shape/dtype/device/그룹은 ValueError. 원본 변경 금지.
    # float64 CPU 출력 및 gradient를 PyTorch grouped Conv와 atol=1e-9로 대조.
    # >>> X02-2
    # TODO X02-2: 바로 위의 입력·출력·보존·실패 조건을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X02-2")
    # <<< X02-2
