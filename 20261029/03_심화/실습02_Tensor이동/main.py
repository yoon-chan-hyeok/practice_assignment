"""실습 02: 모양 변환과 장치 이동 후 같은 장치에서 연산합니다."""
import torch
from torch import nn

torch.manual_seed(42)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
values = torch.arange(12, dtype=torch.float32)
# 12개 원소를 (3,4)로 바꾸고 네 열에 [1,2,3,4]를 더하세요.
# 이후 앞의 두 열을 신경망 입력으로 사용합니다.
# >>> H02
# TODO H02: 위 요구사항을 읽고 이 블록을 완성하세요.
matrix = values.reshape(3, 4)
shifted = matrix
# <<< H02
X = shifted[:, :2].to(device)
y = torch.tensor([0, 0, 1], dtype=torch.long).to(device)
model = nn.Linear(2, 2).to(device)
logits = model(X)
print("행렬:", matrix.tolist())
print("보정:", shifted.tolist())
print("입력/출력:", tuple(X.shape), tuple(logits.shape))
print("device 일치:", X.device == y.device == next(model.parameters()).device)
