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

x = torch.rand(4, 3, 32, 32)
rows = []
for stride in [1, 2]:
    torch.manual_seed(42)
    # BEGIN A02
    # TODO A02: 현재 반복의 stride를 Conv2d에 전달한다.
    conv = nn.Conv2d(3, 8, 3, stride=1, padding=1)
    # END A02
    y = conv(x)
    params = sum(p.numel() for p in conv.parameters())
    # 1 MAC=곱셈 후 누적 1회. bias 덧셈은 제외하며 batch 전체 값이다.
    macs = y.numel() * (3 * 3 * 3)
    rows.append(dict(stride=stride, shape=str(tuple(y.shape)), params=params, macs=macs))
print(pd.DataFrame(rows).to_string(index=False))
pd.DataFrame(rows).to_csv(out / "stride_comparison.csv", index=False)
