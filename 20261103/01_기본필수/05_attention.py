import torch
from torch import nn
torch.set_num_threads(1)  # 작은 CPU 실습의 실행 조건을 고정한다.
torch.manual_seed(42)

x = torch.randn(2,5,16)
attention = nn.MultiheadAttention(16,4,dropout=0.0,batch_first=True)
# TODO B05: 4개 head의 가중치를 평균내지 않고 각각 받는다.
# query/key/value에는 같은 x를 넣는다. average_attn_weights=False를 지정한다.
# BEGIN B05
output, weights = attention(x,x,x,average_attn_weights=True)
# END B05
print("입력:", tuple(x.shape))
print("출력:", tuple(output.shape))
print("head별 weight:", tuple(weights.shape))
print("각 행의 합:", weights[0,0].sum(dim=-1).detach().round(decimals=4))
