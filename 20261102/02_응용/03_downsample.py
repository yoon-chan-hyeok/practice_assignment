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

x = torch.rand(4, 8, 32, 32)
operations = {"pool": nn.MaxPool2d(2), "conv_stride2": nn.Conv2d(8, 8, 3, stride=2, padding=1)}
rows = []
for name, layer in operations.items():
    # BEGIN A03
    # TODO A03: 각 downsampling 층을 입력 x에 적용한다.
    y = x
    # END A03
    rows.append(dict(method=name, shape=str(tuple(y.shape)), params=sum(p.numel() for p in layer.parameters())))
print(pd.DataFrame(rows).to_string(index=False))
pd.DataFrame(rows).to_csv(out / "downsample_comparison.csv", index=False)
