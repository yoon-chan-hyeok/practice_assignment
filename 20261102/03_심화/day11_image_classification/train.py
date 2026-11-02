"""표본 수 가중 학습·평가와 CPU/GPU 계측. 시간은 결과마다 달라질 수 있다."""
import copy
import time
import torch
from torch import nn
from models import set_training_mode

def train_epoch(model, loader, optimizer, device, kind="small"):
    set_training_mode(model, kind)
    loss_sum, correct, count = 0.0, 0, 0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad(set_to_none=True)
        logits = model(images)
        loss = nn.functional.cross_entropy(logits, labels)
        # BEGIN D08
        # TODO D08: 역전파 후 optimizer 갱신을 연결한다.
        pass
        # END D08
        loss_sum += loss.item()*len(labels)
        correct += (logits.argmax(1)==labels).sum().item()
        count += len(labels)
    return loss_sum/count, correct/count

def evaluate(model, loader, device):
    """같은 eval 조건에서 표본 수로 가중 집계하고, 호출 전 모드를 복원한다.

    제공 코드: 검증에서는 optimizer/gradient를 건드리지 않는다. try/finally는
    심화 실습의 상태 보존 계약을 위한 것이며 기본필수의 구현 과제가 아니다.
    """
    flags = {module: module.training for module in model.modules()}
    loss_sum, correct, count = 0.0, 0, 0
    all_logits, all_labels = [], []
    try:
        model.eval()
        with torch.inference_mode():
            for images, labels in loader:
                images, labels = images.to(device), labels.to(device)
                logits = model(images)
                loss_sum += nn.functional.cross_entropy(logits, labels, reduction="sum").item()
                correct += (logits.argmax(1) == labels).sum().item()
                count += len(labels)
                all_logits.append(logits.cpu())
                all_labels.append(labels.cpu())
        if count == 0:
            raise ValueError("평가 표본이 없습니다.")
        return loss_sum/count, correct/count, torch.cat(all_logits), torch.cat(all_labels)
    finally:
        for module, flag in flags.items():
            module.training = flag

def benchmark(model, loader, device, repeats=3):
    """복사 모델로 워밍업 후 매 반복에서 초기 상태·Optimizer를 복원한다."""
    measured = copy.deepcopy(model).to(device)
    initial = {name: value.detach().cpu().clone() for name, value in measured.state_dict().items()}
    x, y = next(iter(loader))
    nn.functional.cross_entropy(measured(x.to(device)), y.to(device)).backward()
    rows = []
    for repeat in range(repeats):
        measured.load_state_dict(initial)
        measured.zero_grad(set_to_none=True)
        measured.train()
        optimizer = torch.optim.SGD(measured.parameters(), lr=0.01)
        if device.type == "cuda":
            torch.cuda.synchronize(device)
            torch.cuda.reset_peak_memory_stats(device)
        start, seen = time.perf_counter(), 0
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad(set_to_none=True)
            nn.functional.cross_entropy(measured(x), y).backward()
            optimizer.step()
            seen += len(y)
        if device.type == "cuda":
            torch.cuda.synchronize(device)
        seconds = time.perf_counter()-start
        rows.append(dict(device=str(device), repeat=repeat, batch=loader.batch_size, samples=seen,
                    seconds=seconds, images_per_second=seen/seconds,
                    peak_vram_mib=torch.cuda.max_memory_allocated(device)/1024**2 if device.type=="cuda" else None,
                    scope="one_epoch_including_loading_and_H2D"))
    return rows
