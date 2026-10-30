import torch
from torch import nn

torch.manual_seed(42)
X = torch.tensor([[1.,2.],[2.,1.],[3.,4.],[4.,3.]])
bn = nn.BatchNorm1d(num_features=8)
model = nn.Sequential(nn.Linear(2, 8), bn, nn.ReLU())
model.train()
# model에 X를 넣어 output을 구하세요. 입력 (4,2)는 Linear에서 (4,8)이 됩니다.
# BatchNorm1d(8)은 8개 특성의 통계를 유지합니다.
# >>> B07
# TODO B07: 위 요구사항에 맞게 이 블록만 완성합니다.
output = X
# <<< B07
print("입력:", tuple(X.shape), "출력:", tuple(output.shape))
print("running_mean:", tuple(bn.running_mean.shape))
before = bn.running_mean.clone()
model.eval()
with torch.no_grad():
    model(X)
print("eval에서 통계 유지:", torch.equal(before, bn.running_mean))
