"""제공 코드: 이 폴더의 실습에 필요한 준비·저장·상태 비교 기반. 다른 실습을 import하지 않는다."""
from pathlib import Path
from contextlib import contextmanager
import copy, hashlib, json, random
import numpy as np
import torch
from torch import nn
ROOT=Path(__file__).resolve().parent

def seed_all(seed=42):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    torch.set_num_threads(1)

def small_model(width=4, batchnorm=False, dropout=0.0):
    return nn.Sequential(nn.Conv2d(3,width,3,padding=1),
        nn.BatchNorm2d(width) if batchnorm else nn.Identity(), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(width,width*2,3,padding=1), nn.ReLU(), nn.Dropout2d(dropout),
        nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Linear(width*2,2))

def synthetic(n=10, seed=7):
    g=torch.Generator().manual_seed(seed)
    return torch.rand(n,3,16,16,generator=g), torch.arange(n)%2

@contextmanager
def preserve_rng():
    py=random.getstate(); npy=np.random.get_state()
    devices=list(range(torch.cuda.device_count())) if torch.cuda.is_available() else []
    try:
        with torch.random.fork_rng(devices=devices): yield
    finally:
        random.setstate(py); np.random.set_state(npy)

def snapshot(model):
    return dict(state=copy.deepcopy(model.state_dict()), modes={n:m.training for n,m in model.named_modules()},
        grads={n:None if p.grad is None else p.grad.clone() for n,p in model.named_parameters()},
        requires={n:p.requires_grad for n,p in model.named_parameters()})

def restore_snapshot(model,saved):
    model.load_state_dict(saved['state'])
    for n,p in model.named_parameters():
        p.requires_grad_(saved['requires'][n])
        p.grad=None if saved['grads'][n] is None else saved['grads'][n].clone()
    for n,m in model.named_modules(): m.training=saved['modes'][n]

def save_json(name,value,out=None):
    out=Path(out) if out is not None else ROOT/'outputs'; out.mkdir(parents=True,exist_ok=True)
    (out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')

def fingerprint():
    d=hashlib.sha256()
    for split in ('train','valid'):
        for p in sorted((ROOT/'data'/split).rglob('*.png')):
            d.update(p.relative_to(ROOT/'data').as_posix().encode());d.update(p.read_bytes())
    return d.hexdigest()

def image_dataset(split='train', augment=False, with_index=False):
    from torchvision import datasets,transforms
    if split not in ('train','valid'): raise ValueError('학습·개발용 train/valid만 사용합니다.')
    ops=[transforms.Resize((32,32))]
    if augment:
        if split!='train': raise ValueError('무작위 증강은 train만 허용합니다.')
        ops.append(transforms.RandomHorizontalFlip())
    ops.append(transforms.ToTensor())
    ds=datasets.ImageFolder(ROOT/'data'/split,transform=transforms.Compose(ops))
    return IndexedDataset(ds) if with_index else ds

class IndexedDataset(torch.utils.data.Dataset):
    def __init__(self,base): self.base=base
    def __len__(self): return len(self.base)
    def __getitem__(self,index):
        x,y=self.base[index]
        return x,y,index

def seed_worker(worker_id):
    value=torch.initial_seed()%2**32
    random.seed(value);np.random.seed(value)
