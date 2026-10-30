"""실습 03: x=3에서 y=x²+2x+1과 기울기를 계산합니다."""
import torch
x = torch.tensor(3.0, requires_grad=True)
# y = x² + 2x + 1을 Tensor 연산으로 작성하세요.
# x를 Python 숫자로 바꾸지 마세요. 계산 그래프가 이어져 있어야 합니다.
# >>> B03
# TODO B03: 위 요구사항을 읽고 이 블록을 완성하세요.
y = x + 0
# <<< B03
# backward는 y 값을 바꾸지 않고 x.grad에 기울기를 계산합니다.
y.backward()
print("y:", y.item())
print("dy/dx:", x.grad.item())
