from pathlib import Path
import copy
import csv
import json
import time
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import pandas as pd

torch.manual_seed(42)
torch.set_num_threads(1)
root = Path(__file__).resolve().parent
out = root / "outputs"
out.mkdir(exist_ok=True)

transform = transforms.Compose([transforms.Resize((32, 32)), transforms.ToTensor()])
train = datasets.ImageFolder(root / "data" / "train", transform=transform)
valid = datasets.ImageFolder(root / "data" / "valid", transform=transform)
train_loader = DataLoader(train, batch_size=16, shuffle=True, num_workers=0,
                          generator=torch.Generator().manual_seed(42))
valid_loader = DataLoader(valid, batch_size=16, shuffle=False, num_workers=0)

# 측정: 데이터 파일 읽기 + H2D + forward/backward/step. 준비·워밍업·모델 복원은 제외.
initial_model = nn.Sequential(
    nn.Conv2d(3, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Linear(32, 2),
)
initial_state = copy.deepcopy(initial_model.state_dict())
devices = ["cpu"] + (["cuda"] if torch.cuda.is_available() else [])
rows = []
for device_name in devices:
    device = torch.device(device_name)
    model = copy.deepcopy(initial_model).to(device)
    warm_x, warm_y = next(iter(DataLoader(train, batch_size=16)))
    nn.functional.cross_entropy(model(warm_x.to(device)), warm_y.to(device)).backward()
    model.load_state_dict(initial_state)
    model.zero_grad(set_to_none=True)
    for repeat in range(3):
        model.load_state_dict(initial_state)
        optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
        loader = DataLoader(train, batch_size=16, shuffle=False, num_workers=0)
        if device.type == "cuda":
            torch.cuda.synchronize(device)
            torch.cuda.reset_peak_memory_stats(device)
        start = time.perf_counter()
        seen = 0
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            nn.functional.cross_entropy(model(images), labels).backward()
            optimizer.step()
            seen += len(labels)
        # BEGIN A07
        # TODO A07: GPU 작업 완료를 기다린 후 종료 시간을 읽는다.
        pass
        # END A07
        seconds = time.perf_counter()-start
        peak = torch.cuda.max_memory_allocated(device)/1024**2 if device.type=="cuda" else None
        rows.append(dict(device=device_name, repeat=repeat, images=seen, batch_size=16,
                         seconds=seconds, images_per_second=seen/seconds, peak_vram_mib=peak,
                         scope="one_epoch_including_loading_and_transfer"))
pd.DataFrame(rows).to_csv(out / "hardware_benchmark.csv", index=False)
print(pd.DataFrame(rows).round(4).to_string(index=False))
if not torch.cuda.is_available():
    print("GPU: N/A (실제 CUDA 미측정, 0초로 기록하지 않음)")
