"""실습 05 · 제공된 CNN으로 5 epoch 학습한다. test는 읽지 않는다."""
from pathlib import Path
import copy
import torch
from torch import nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

root = Path(__file__).resolve().parent
torch.manual_seed(42)
torch.set_num_threads(1)
transform = transforms.Compose([transforms.Resize((32, 32)), transforms.ToTensor()])
train = datasets.ImageFolder(root / "data" / "train", transform=transform)
valid = datasets.ImageFolder(root / "data" / "valid", transform=transform)
# 작은 정상 데이터는 한 배치로 읽어 학습 순서를 단순하게 관찰한다.
x_train, y_train = next(iter(DataLoader(train, batch_size=len(train), shuffle=False)))
x_valid, y_valid = next(iter(DataLoader(valid, batch_size=len(valid), shuffle=False)))

model = nn.Sequential(
    nn.Conv2d(3, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Linear(32, 2),
)
optimizer = torch.optim.AdamW(model.parameters(), lr=0.01, weight_decay=0.0)
loss_fn = nn.CrossEntropyLoss()
best_loss = float("inf")
for epoch in range(1, 6):
    model.train()
    optimizer.zero_grad()
    logits = model(x_train)
    loss = loss_fn(logits, y_train)
    # 해설 B05: backward는 미분값 계산, step은 그 값을 이용한 갱신이다.
    # BEGIN B05
    # TODO B05: loss를 역전파하고 optimizer로 한 번 갱신한다.
    pass
    # END B05
    model.eval()
    with torch.no_grad():
        train_loss = loss_fn(model(x_train), y_train).item()
        valid_logits = model(x_valid)
        valid_loss = loss_fn(valid_logits, y_valid).item()
        valid_acc = (valid_logits.argmax(1) == y_valid).float().mean().item()
    print(f"epoch={epoch} train_loss={train_loss:.4f} valid_loss={valid_loss:.4f} valid_acc={valid_acc:.2f}")
    if valid_loss < best_loss:
        best_loss, best_epoch = valid_loss, epoch
        best_state = copy.deepcopy(model.state_dict())
model.load_state_dict(best_state)
print("선택한 epoch:", best_epoch)
