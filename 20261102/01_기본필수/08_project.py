"""실습 08 · 한 파일로 학습·best 복원·CSV·가중치 저장을 마친다.
모델/입력/저장 코드는 제공된다. 추가 함수·클래스·예외처리를 만들지 않는다.
"""
from pathlib import Path
import copy
import json
import time
import torch
from torch import nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import pandas as pd

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
history = []
best_loss = float("inf")
start = time.perf_counter()
for epoch in range(1, 6):
    model.train()
    optimizer.zero_grad()
    # BEGIN B08
    # TODO B08: model 순전파 후 정답과 CrossEntropyLoss를 계산한다.
    logits = model(x_train)
    loss = logits.sum() * 0
    # END B08
    # BEGIN B09
    # TODO B09: 역전파 후 가중치를 갱신한다.
    pass
    # END B09
    model.eval()
    with torch.no_grad():
        train_logits = model(x_train)
        valid_logits = model(x_valid)
        train_loss = loss_fn(train_logits, y_train).item()
        valid_loss = loss_fn(valid_logits, y_valid).item()
        train_acc = (train_logits.argmax(1) == y_train).float().mean().item()
        valid_acc = (valid_logits.argmax(1) == y_valid).float().mean().item()
    history.append(dict(epoch=epoch, train_loss=train_loss, valid_loss=valid_loss,
                        train_accuracy=train_acc, valid_accuracy=valid_acc))
    if valid_loss < best_loss:
        best_loss, best_epoch = valid_loss, epoch
        best_state = copy.deepcopy(model.state_dict())
seconds = time.perf_counter() - start
model.load_state_dict(best_state)
model.eval()
with torch.no_grad():
    logits = model(x_valid)
    predictions = logits.argmax(1)
    accuracy = (predictions == y_valid).float().mean().item()
history_table = pd.DataFrame(history)
history_table["is_best"] = history_table["epoch"] == best_epoch
history_table.to_csv(root / "history.csv", index=False)
pd.DataFrame([dict(model="SmallCNN", input_size=32, trainable_params=5154,
                   best_epoch=best_epoch, valid_loss=best_loss, valid_accuracy=accuracy,
                   training_seconds=seconds, device="cpu")]).to_csv(root / "model_comparison.csv", index=False)
pd.DataFrame(dict(file=[Path(p).name for p, _ in valid.samples], actual=y_valid.tolist(),
                  predicted=predictions.tolist())).to_csv(root / "valid_predictions.csv", index=False)
# 가중치뿐 아니라 클래스 순서와 전처리 정보도 함께 저장한다.
# class_to_idx와 같은 순서의 classes로 0/1 라벨의 뜻을 보존한다.
torch.save(dict(state_dict=best_state, classes=train.classes, class_to_idx=train.class_to_idx,
                image_size=32, normalize=None, architecture="conv16_conv32_gap_fc2",
                best_epoch=best_epoch), root / "best_model.pt")
print(history_table.drop(columns="is_best").round(4).to_string(index=False))
print("best epoch:", best_epoch, "valid accuracy:", round(accuracy, 4))
print("저장: history.csv, model_comparison.csv, valid_predictions.csv, best_model.pt")
print("test 4장은 읽거나 모델에 전달하지 않았다.")
