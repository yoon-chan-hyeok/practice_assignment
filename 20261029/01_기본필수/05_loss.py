"""실습 05: 정답 인덱스와 logits로 손실을 계산합니다."""
import torch
from torch import nn

logits = torch.tensor([[2.0, 0.0], [0.0, 2.0]])
target = torch.tensor([0, 1], dtype=torch.long)
loss_fn = nn.CrossEntropyLoss()
# loss_fn에 logits와 target을 순서대로 넣어 loss를 계산하세요.
# logits에 softmax를 먼저 적용하지 마세요.
# >>> B05
# TODO B05: 위 요구사항을 읽고 이 블록을 완성하세요.
loss = torch.tensor(0.0)
# <<< B05
print("logits:", tuple(logits.shape))
print("target:", tuple(target.shape), target.dtype)
print("loss:", round(loss.item(), 6))
