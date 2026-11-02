import torch
from torch import nn
torch.set_num_threads(1)  # 작은 CPU 실습의 실행 조건을 고정한다.
torch.manual_seed(42)
# 원리용 독립 Sequence 20개. 증가=1, 감소=0, 가운데 평균은 거의 같다.
g = torch.Generator().manual_seed(1203)
y_all = torch.tensor([0,1]*10)
base = torch.linspace(-1,1,6)
x_all = torch.stack([(2*y-1)*base for y in y_all]).unsqueeze(-1)
x_all = x_all + 0.03*torch.randn(20,6,1,generator=g)
x_train,y_train = x_all[:12],y_all[:12]
x_valid,y_valid = x_all[12:16],y_all[12:16]
# 마지막 4개는 보관. 함수에 전달하지 않는다.

for kind in ["RNN","LSTM"]:
    torch.manual_seed(42)
    core = nn.RNN(1,8,batch_first=True) if kind=="RNN" else nn.LSTM(1,8,batch_first=True)
    head = nn.Linear(8,2)
    parameters = list(core.parameters())+list(head.parameters())
    optimizer = torch.optim.Adam(parameters,lr=0.02)
    for epoch in range(30):
        optimizer.zero_grad()
        output,_ = core(x_train)
        loss = nn.CrossEntropyLoss()(head(output[:,-1]),y_train)
        # TODO B06: 손실의 gradient를 구한 뒤 모델과 head를 갱신한다.
        # backward가 gradient를 계산하고 optimizer.step이 가중치를 바꾼다.
        # BEGIN B06
        pass
        # END B06
    core.eval(); head.eval()
    with torch.inference_mode():
        output,_ = core(x_valid)
        pred = head(output[:,-1]).argmax(dim=1)
    print(kind,"params:",sum(p.numel() for p in parameters),
          "valid 정답:",y_valid.tolist(),"예측:",pred.tolist(),
          "accuracy:",round((pred==y_valid).float().mean().item(),3))
