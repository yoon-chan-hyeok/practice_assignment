"""실습 05: 마지막 작은 batch를 버리지 않고 자료를 모두 읽습니다."""
from pathlib import Path
import csv
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader

X = torch.arange(20, dtype=torch.float32).reshape(10, 2) / 10
y = torch.tensor([0, 0, 0, 0, 0, 1, 1, 1, 1, 1], dtype=torch.long)
dataset = TensorDataset(X, y)
# dataset을 batch_size=4, shuffle=False, drop_last=False로 공급하세요.
# 정상 데이터 10건이 4·4·2로 나뉘어야 합니다. num_workers=0을 유지합니다.
# >>> A05
# TODO A05: 위 요구사항을 읽고 이 블록을 완성하세요.
loader = DataLoader(dataset, batch_size=5, shuffle=False, num_workers=0)
# <<< A05
sizes = []
for index, (xb, yb) in enumerate(loader, 1):
    sizes.append([index, len(yb)])
    print(index, tuple(xb.shape), tuple(yb.shape))
print("합계:", sum(n for _, n in sizes))
logits = torch.tensor([[2., 0.], [0., 2.]])
print("예시 CE:", round(nn.CrossEntropyLoss()(logits, torch.tensor([0, 1])).item(), 6))
out = Path(__file__).resolve().parent / "outputs"
out.mkdir(exist_ok=True)
with (out / "batch_sizes.csv").open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f); writer.writerow(["batch", "samples"]); writer.writerows(sizes)

# 추가 A09: 배치 크기가 다를 때 평균 loss를 합치는 방법입니다.
# 입력: 평균 손실 [0.1, 0.2, 0.9], 각 배치의 표본 수 [4, 4, 2].
# 요구: loss × 실제 표본 수의 합을 전체 표본 수로 나누세요.
# 금지: 배치 평균 세 개를 단순 평균하거나 마지막 배치를 4건으로 계산하지 않습니다.
# 완료: weighted_loss=0.3. 잘못된 단순 평균 0.4와 차이를 설명합니다.
loss_means = [0.1, 0.2, 0.9]
sample_counts = [4, 4, 2]
# >>> A09
# TODO A09: 배치 크기까지 반영한 평균을 계산하세요.
weighted_loss = 0.0
# <<< A09
print("샘플 가중 loss:", round(weighted_loss, 6))
print("배치 단순 평균:", round(sum(loss_means) / len(loss_means), 6))
