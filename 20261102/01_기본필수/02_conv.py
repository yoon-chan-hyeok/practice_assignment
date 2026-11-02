"""실습 02 · 공간 크기를 유지하고 특징 채널을 8개 만든다."""
import torch
from torch import nn

torch.manual_seed(42)
x = torch.rand(4, 3, 32, 32)
# Conv2d의 필수: 입력 채널, 출력 채널, 커널 크기.
# padding=1은 선택 인자. 3×3, stride=1과 결합하면 높이·너비를 유지한다.
# BEGIN B02
# TODO B02: 3입력·8출력·3×3·padding 1의 합성곱 층을 만든다.
conv = nn.Conv2d(3, 8, 3)
# END B02
y = conv(x)
print("입력:", tuple(x.shape))
print("출력:", tuple(y.shape))
print("파라미터:", sum(p.numel() for p in conv.parameters()))
