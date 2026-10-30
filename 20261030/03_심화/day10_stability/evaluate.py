"""제공 평가 코드. train/eval과 gradient 추적은 별개의 상태입니다."""
import torch
from torch import nn

def evaluate(model, X, y, device):
    modes = [(m, m.training) for m in model.modules()]
    try:
        model.eval()
        with torch.no_grad():
            logits = model(X.to(device))
            loss = nn.functional.cross_entropy(logits, y.to(device)).item()
            prediction = logits.argmax(1).cpu()
        return loss, (prediction == y.cpu()).float().mean().item(), prediction
    finally:
        # train(flag)는 자식까지 덮으므로 개별 모드를 직접 복구합니다.
        for module, mode in modes:
            module.training = mode
