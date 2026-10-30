"""제공 코드: CSV의 고정 분할만 사용합니다. test 입력·정답 Tensor는 만들지 않습니다."""
from pathlib import Path
import csv
import torch
from torch.utils.data import TensorDataset, DataLoader

BASE = Path(__file__).resolve().parent
CONFIG = {"seed":42,"hidden":8,"epochs":80,"batch_size":32,"lr":0.1,
          "optimizer":"SGD","dataset":"day9_points200_v1"}

def load_development():
    with (BASE/"data"/"points.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    split_ids = {name:[r["id"] for r in rows if r["split"]==name] for name in ("train","valid","test")}
    tensors = {}
    for name in ("train","valid"):
        part = [r for r in rows if r["split"]==name]
        X = torch.tensor([[float(r["x1"]),float(r["x2"])] for r in part],dtype=torch.float32)
        y = torch.tensor([int(r["label"]) for r in part],dtype=torch.long)
        tensors[name]=(X,y)
    return tensors, split_ids

def make_loaders(tensors, generator):
    train=DataLoader(TensorDataset(*tensors["train"]),batch_size=CONFIG["batch_size"],shuffle=True,
                     generator=generator,num_workers=0,drop_last=False)
    valid=DataLoader(TensorDataset(*tensors["valid"]),batch_size=CONFIG["batch_size"],shuffle=False,num_workers=0)
    return train, valid
