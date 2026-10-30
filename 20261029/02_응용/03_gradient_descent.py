"""실습 03: 매번 새로운 그래프를 만들고 gradient를 비웁니다."""
from pathlib import Path
import csv
import torch

w = torch.tensor(0.0, requires_grad=True)
lr = 0.1
history = []
for step in range(1, 11):
    loss = (w - 4.0) ** 2
    loss.backward()
    with torch.no_grad():
        # w에서 학습률 × 현재 기울기를 빼세요.
        # 여기는 no_grad 블록 안입니다. 새 값으로 Tensor 객체를 교체하지 말고 w를 직접 갱신하세요.
        # >>> A03
        # TODO A03: 위 요구사항을 읽고 이 블록을 완성하세요.
        pass
        # <<< A03
    w.grad.zero_()
    # 아래 loss는 갱신한 w에서 다시 계산한 값입니다.
    history.append([step, w.item(), (w.detach() - 4.0).square().item()])
for step, value, loss_after in history:
    print(step, round(value, 6), round(loss_after, 6))
out = Path(__file__).resolve().parent / "outputs"
out.mkdir(exist_ok=True)
with (out / "gd_history.csv").open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f); writer.writerow(["step", "w_after", "loss_after"]); writer.writerows(history)
