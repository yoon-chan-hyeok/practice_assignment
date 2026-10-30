"""실습 04: 같은 파라미터의 Module과 Sequential을 비교합니다."""
import torch
from torch import nn

class SimpleANN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(2,8), nn.ReLU(), nn.Linear(8,2))

    def forward(self, x):
        # 입력 x를 self.net에 넣은 결과를 반환하세요.
        # 출력은 (N,2) logits이며 softmax를 추가하지 않습니다.
        # >>> H04
        # TODO H04: 위 요구사항을 읽고 이 블록을 완성하세요.
        return x
        # <<< H04

torch.manual_seed(42)
custom = SimpleANN()
sequential = nn.Sequential(nn.Linear(2,8), nn.ReLU(), nn.Linear(8,2))
# 서로 다른 랜덤 초기값을 비교하지 않도록 같은 값을 복사합니다.
sequential.load_state_dict(custom.net.state_dict())
X = torch.tensor([[1.,2.], [0.,1.], [-1.,0.]])
a, b = custom(X), sequential(X)
print("출력 shape:", tuple(a.shape), tuple(b.shape))
print("동일 출력:", torch.allclose(a, b))
print("파라미터:", sum(p.numel() for p in custom.parameters()))
