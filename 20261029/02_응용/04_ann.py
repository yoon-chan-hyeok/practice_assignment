"""실습 04: 은닉 너비에 따라 파라미터 수가 변합니다. 학습 성능 비교는 아닙니다."""
import torch
from torch import nn

torch.manual_seed(42)
X = torch.ones(4, 2)
for hidden in [4, 8, 16]:
    # hidden 값을 사용해 입력 2개 → 은닉 hidden개 → 출력 2개를 연결하세요.
    # 은닉층 뒤에 ReLU를 넣고 마지막에 softmax는 넣지 않습니다.
    # >>> A04
    # TODO A04: 위 요구사항을 읽고 이 블록을 완성하세요.
    model = nn.Sequential(nn.Linear(2, hidden), nn.Linear(hidden, 2))
    # <<< A04
    logits = model(X)
    count = sum(p.numel() for p in model.parameters())
    print("은닉:", hidden, "출력:", tuple(logits.shape), "파라미터:", count)
