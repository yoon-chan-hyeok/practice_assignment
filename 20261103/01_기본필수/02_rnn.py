import torch
from torch import nn
torch.set_num_threads(1)  # 작은 CPU 실습의 실행 조건을 고정한다.
torch.manual_seed(42)

x = torch.randn(4,6,3)
rnn = nn.RNN(3,8,batch_first=True)
output, h_n = rnn(x)  # 모든 시점 출력과 마지막 은닉 상태를 따로 받는다.
# TODO B02: 은닉 특성 8개를 두 클래스의 점수로 바꾸는 층을 만든다.
# 필수 위치 인자: in_features=8, out_features=2; bias=True는 기본 선택값.
# BEGIN B02
head = nn.Linear(8, 1)
# END B02
logits = head(h_n[-1])  # 마지막 층의 상태: [4,8]
print("입력:", tuple(x.shape))
print("output / h_n:", tuple(output.shape), tuple(h_n.shape))
print("logits:", tuple(logits.shape))
print("마지막 시점 일치:", torch.allclose(output[:,-1],h_n[-1]))
