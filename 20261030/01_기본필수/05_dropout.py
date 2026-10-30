import torch
from torch import nn

torch.manual_seed(42)
X = torch.ones(2, 4)
dropout = nn.Dropout(p=0.5)
dropout.train()
for i in range(3):
    print("train", i + 1, dropout(X).tolist())
# Dropout을 평가 모드로 바꾸세요. dropout.eval()은 mode만 바꿉니다.
# 평가 모드의 Dropout은 입력을 그대로 전달하며, gradient 비활성화와는 별개의 기능입니다.
# >>> B06
# TODO B06: 위 요구사항에 맞게 이 블록만 완성합니다.
pass
# <<< B06
for i in range(3):
    print("eval", i + 1, dropout(X).tolist())
