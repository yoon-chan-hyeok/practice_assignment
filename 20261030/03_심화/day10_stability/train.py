"""학습, Scheduler, Early Stopping, best snapshot을 한 실험으로 묶습니다."""
import copy
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader
from model import build_model
from evaluate import evaluate

def fit(config, X, y, Xv, yv, device):
    torch.manual_seed(config["seed"])
    model = build_model(config).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config["lr"], weight_decay=config["weight_decay"])
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode="min", factor=.5, patience=3, threshold=1e-4, threshold_mode="abs")
    generator = torch.Generator().manual_seed(config["seed"]+1)
    loader = DataLoader(TensorDataset(X, y), batch_size=config["batch_size"], shuffle=True,
                        generator=generator, num_workers=0)
    best_loss = float("inf")
    patience_reference = float("inf")
    bad_epochs = 0
    history = []
    for epoch in range(1, config["epochs"]+1):
        model.train()
        total_loss = 0.0
        lr_used = optimizer.param_groups[0]["lr"]
        for xb, yb in loader:
            xb, yb = xb.to(device), yb.to(device)
            optimizer.zero_grad()
            loss = nn.functional.cross_entropy(model(xb), yb)
            # 배치 loss의 역전파 후 optimizer로 파라미터를 갱신하세요.
            # loss는 배치 평균입니다. 로그 집계에서는 loss.item()*배치건수를 누적해야 합니다.
            # >>> S07
            # TODO S07: 위 요구사항에 맞게 이 블록만 완성합니다.
            pass
            # <<< S07
            total_loss += loss.item()*len(yb)
        train_loss, _, _ = evaluate(model, X, y, device)
        valid_loss, valid_acc, _ = evaluate(model, Xv, yv, device)
        scheduler.step(valid_loss)
        if valid_loss < best_loss:
            # 관측한 valid loss가 더 작을 때 state_dict를 copy.deepcopy로 보관하세요.
            # 단순 대입은 이후 학습에 따라 바뀌므로 best_state가 최적 epoch를 보존하지 못합니다.
            # 이 best는 관측 최소값이고, patience 재설정용 min_delta 기준은 별도입니다.
            # >>> S08
            # TODO S08: 위 요구사항에 맞게 이 블록만 완성합니다.
            best_loss = valid_loss
            best_epoch = epoch
            best_state = model.state_dict()
            # <<< S08
        # min_delta를 넘는 개선이 있을 때만 patience 카운터를 초기화합니다.
        if valid_loss < patience_reference-config["min_delta"]:
            patience_reference = valid_loss
            bad_epochs = 0
        else:
            bad_epochs += 1
        history.append({"epoch":epoch,"train_loss_step":total_loss/len(y),
                        "train_loss_eval":train_loss,"valid_loss":valid_loss,"valid_acc":valid_acc,
                        "lr_used":lr_used,"lr_next":optimizer.param_groups[0]["lr"],"bad_epochs":bad_epochs})
        if bad_epochs >= config["patience"]:
            break
    # 마지막 epoch의 파라미터와 best는 다를 수 있습니다.
    model.load_state_dict(best_state)
    restored_loss, restored_acc, prediction = evaluate(model, Xv, yv, device)
    summary = {"name":config["name"],"best_epoch":best_epoch,"best_valid_loss":best_loss,
               "restored_valid_loss":restored_loss,"valid_acc_at_best":restored_acc,
               "stop_epoch":epoch,"last_valid_loss":valid_loss,"test_used":False}
    return model, history, summary, prediction
