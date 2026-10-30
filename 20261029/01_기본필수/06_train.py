"""실습 06: 작은 정상 자료로 학습 순서만 익힙니다. 여기는 train 오차 확인용입니다."""
import torch
from torch import nn

torch.manual_seed(42)
X = torch.tensor([[-2., -1.], [-1., -1.], [-1., 0.], [0., -1.],
                  [1., 0.], [0., 1.], [1., 1.], [2., 1.]])
y = torch.tensor([0, 0, 0, 0, 1, 1, 1, 1], dtype=torch.long)
model = nn.Sequential(nn.Linear(2, 8), nn.ReLU(), nn.Linear(8, 2))
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
print("학습 전 loss:", round(loss_fn(model(X), y).item(), 6))
model.train()
for epoch in range(80):
    optimizer.zero_grad()
    loss = loss_fn(model(X), y)
    # 현재 loss의 gradient를 계산하세요.
    # 파라미터 값은 아직 바뀌지 않으며 .grad에 기울기가 들어갑니다.
    # >>> B06
    # TODO B06: 위 요구사항을 읽고 이 블록을 완성하세요.
    pass
    # <<< B06
    # 현재 gradient를 사용해 파라미터를 한 번 갱신하세요.
    # optimizer의 step 메서드를 호출합니다.
    # >>> B07
    # TODO B07: 위 요구사항을 읽고 이 블록을 완성하세요.
    pass
    # <<< B07
model.eval()
with torch.no_grad():
    logits = model(X)
    print("학습 후 loss:", round(loss_fn(logits, y).item(), 6))
    print("train 정확도:", round((logits.argmax(dim=1) == y).float().mean().item(), 4))
print("주의: 위 정확도는 학습한 8건의 결과이며 새로운 자료의 성능이 아닙니다.")
