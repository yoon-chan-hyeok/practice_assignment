"""제공 학습 루프. Loss와 지표의 측정 시점·best 선택 기준을 명시한다."""
from copy import deepcopy
from time import perf_counter
import torch
from torch import nn

def evaluate(model, batch, task):
    """제공 평가 함수: 평가 후 각 하위 모듈의 원래 train/eval 상태를 복구한다."""
    modes=[(module,module.training) for module in model.modules()]
    try:
        model.eval()
        with torch.inference_mode():
            predicted=model(batch['x'],batch['lengths'])
            criterion=nn.CrossEntropyLoss() if task=='classification' else nn.MSELoss()
            loss=criterion(predicted,batch['y']).item()
            accuracy=(predicted.argmax(1)==batch['y']).float().mean().item() if task=='classification' else None
        return loss,accuracy,predicted.detach().clone()
    finally:
        # 부모 train()의 재귀 호출로 섞인 모드를 덮지 않고 각 모드를 복구한다.
        for module,mode in modes:
            module.training=mode

def fit(model, data, task='regression', epochs=30, lr=0.02):
    optimizer=torch.optim.Adam(model.parameters(),lr=lr)
    criterion=nn.CrossEntropyLoss() if task=='classification' else nn.MSELoss()
    best=float('inf'); best_epoch=0; history=[]; start=perf_counter()
    for epoch in range(1,epochs+1):
        model.train(); optimizer.zero_grad(set_to_none=True)
        batch=data['train']; predicted=model(batch['x'],batch['lengths'])
        loss=criterion(predicted,batch['y']); loss.backward(); optimizer.step()
        # 같은 epoch가 끝난 eval 모드에서 train과 valid를 모두 측정한다.
        train_loss,_,_=evaluate(model,data['train'],task)
        valid_loss,acc,_=evaluate(model,data['valid'],task)
        history.append({'epoch':epoch,'train_loss':train_loss,'valid_loss':valid_loss,'valid_accuracy':acc})
        if valid_loss < best:
            best=valid_loss; best_epoch=epoch; state=deepcopy(model.state_dict())
    elapsed=perf_counter()-start
    model.load_state_dict(state)
    loss,acc,pred=evaluate(model,data['valid'],task)
    return {'history':history,'best_epoch':best_epoch,'valid_loss':loss,'valid_accuracy':acc,
            'prediction':pred,'state':state,'seconds':elapsed,
            'params':sum(p.numel() for p in model.parameters())}
