"""실습 03: 수동 Gradient Descent와 gradient 누적을 구분합니다."""
from pathlib import Path
import csv
import torch

w = torch.tensor(0.0, requires_grad=True)
records = []
for step in range(1, 11):
    before = w.item()
    loss = (w - 4) ** 2
    loss.backward()
    gradient = w.grad.item()
    with torch.no_grad():
        # lr=0.1로 w를 갱신하세요. 아래 grad.zero_()는 다음 반복에 이전 기울기가 섞이지 않게 합니다.
        # >>> H03
        # TODO H03: 위 요구사항을 읽고 이 블록을 완성하세요.
        pass
        # <<< H03
    w.grad.zero_()
    records.append([step, before, gradient, w.item(), (w.detach()-4).square().item()])
for r in records:
    print(r[0], round(r[1], 6), round(r[2], 6), round(r[3], 6), round(r[4], 6))
u = torch.tensor(1.0, requires_grad=True)
(u**2).backward()
first = u.grad.item()
# 같은 그래프를 다시 쓰는 대신 새로운 순전파 그래프를 만듭니다.
(u**2).backward()
print("초기화하지 않은 gradient:", first, "->", u.grad.item())
out = Path(__file__).resolve().parent / "outputs"
out.mkdir(exist_ok=True)
with (out / "updates.csv").open("w", encoding="utf-8-sig", newline="") as f:
    writer=csv.writer(f); writer.writerow(["step","w_before","gradient","w_after","loss_after"]); writer.writerows(records)
