"""실습 05: 배치 평균들의 단순 평균이 아닌 샘플 수 가중 평균을 계산합니다."""
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader

logits = torch.tensor([[3.,0.]]*8 + [[0.,3.]]*2)
y = torch.zeros(10, dtype=torch.long)
loader = DataLoader(TensorDataset(logits, y), batch_size=4, shuffle=False)
loss_fn = nn.CrossEntropyLoss()
total_loss, count = 0.0, 0
batch_means = []
for xb, yb in loader:
    loss = loss_fn(xb, yb)
    # 현재 배치 평균 loss에 실제 배치 행 수를 곱해 total_loss에 더하세요.
    # 마지막 배치는 2행입니다. batch_size=4를 곱하면 안 됩니다.
    # >>> H05
    # TODO H05: 위 요구사항을 읽고 이 블록을 완성하세요.
    total_loss += loss.item()
    # <<< H05
    count += len(yb)
    batch_means.append(loss.item())
print("배치 크기: 4, 4, 2")
print("잘못된 단순 평균:", round(sum(batch_means)/len(batch_means), 6))
print("샘플 가중 평균:", round(total_loss/count, 6))
print("전체를 한 번에 계산:", round(loss_fn(logits, y).item(), 6))
