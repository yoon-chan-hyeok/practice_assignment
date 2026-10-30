"""실습 04: 2 → 8 → 2 신경망의 순전파를 확인합니다."""
import torch
from torch import nn

torch.manual_seed(42)
# Sequential의 마지막 Linear를 수정해 출력 클래스 수가 2가 되게 하세요.
# 첫 Linear(2, 8)와 ReLU는 그대로 두세요. 모델 정의는 미리 제공했습니다.
# >>> B04
# TODO B04: 위 요구사항을 읽고 이 블록을 완성하세요.
model = nn.Sequential(nn.Linear(2, 8), nn.ReLU(), nn.Linear(8, 1))
# <<< B04
X = torch.tensor([[1.0, 2.0], [3.0, 4.0], [0.0, 1.0], [2.0, 0.0]])
logits = model(X)
print("입력:", tuple(X.shape))
print("출력:", tuple(logits.shape))
print("파라미터 수:", sum(p.numel() for p in model.parameters()))
# logits는 원시 점수입니다. 이 시점에는 학습하지 않았습니다.
