"""제공 코드: split을 다시 만들지 않고 train·valid만 Tensor로 반환합니다."""
from pathlib import Path
import pandas as pd
import torch

def load_data(path):
    df = pd.read_csv(path)
    tr = df[df["split"] == "train"]
    va = df[df["split"] == "valid"]
    X = torch.tensor(tr[["x1", "x2"]].values, dtype=torch.float32)
    y = torch.tensor(tr["label"].values, dtype=torch.long)
    Xv = torch.tensor(va[["x1", "x2"]].values, dtype=torch.float32)
    yv = torch.tensor(va["label"].values, dtype=torch.long)
    return X, y, Xv, yv, va["id"].tolist()
