"""실습 07 · CPU 한 epoch. 디스크 로딩 포함, 워밍업과 초기화 시간은 제외한다."""
from pathlib import Path
import copy
import time
import csv
import torch
from torch import nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

torch.manual_seed(42)
torch.set_num_threads(1)
root = Path(__file__).resolve().parent
transform = transforms.Compose([transforms.Resize((32, 32)), transforms.ToTensor()])
train = datasets.ImageFolder(root / "data" / "train", transform=transform)
loader = DataLoader(train, batch_size=4, shuffle=False, num_workers=0)
model = nn.Sequential(
    nn.Conv2d(3, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Linear(32, 2),
)
loss_fn = nn.CrossEntropyLoss()
# 워밍업은 복사본에서만 수행하므로 측정 모델의 초기값은 바뀌지 않는다.
warm = copy.deepcopy(model)
warm_x, warm_y = next(iter(loader))
loss_fn(warm(warm_x), warm_y).backward()
del warm
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
seen = 0
start = time.perf_counter()
for images, labels in loader:
    optimizer.zero_grad()
    loss_fn(model(images), labels).backward()
    optimizer.step()
    seen += len(labels)
seconds = time.perf_counter() - start
# BEGIN B07
# TODO B07: 처리한 이미지 수를 경과 초로 나눠 images/s를 구한다.
throughput = 0.0
# END B07
print("CPU 이미지 수:", seen)
print(f"시간={seconds:.6f}s, 처리량={throughput:.2f} images/s, GPU VRAM=N/A")
with (root / "hardware_benchmark.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["device", "images", "batch_size", "seconds", "images_per_second", "peak_vram_mib", "scope"])
    writer.writerow(["cpu", seen, 4, seconds, throughput, "", "one_epoch_including_image_loading"])
