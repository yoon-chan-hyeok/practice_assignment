"""제공 코드: 상태 보존·결과 저장. 이 파일은 해당 교시의 구현 대상이 아니다."""
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
import json, random
import numpy as np
import torch

def capture_rng():
    kind,keys,pos,has_gauss,cached=np.random.get_state()
    return {'torch':torch.get_rng_state().clone(),
            'cuda':torch.cuda.get_rng_state_all() if torch.cuda.is_available() else [],
            'python':random.getstate(),
            'numpy':{'kind':kind,'keys':torch.tensor(keys.astype(np.int64)),'pos':pos,'has_gauss':has_gauss,'cached':float(cached)}}

def restore_rng(s):
    torch.set_rng_state(s['torch'])
    if s['cuda']: torch.cuda.set_rng_state_all(s['cuda'])
    random.setstate(s['python']); n=s['numpy']
    np.random.set_state((n['kind'],n['keys'].numpy().astype(np.uint32),n['pos'],n['has_gauss'],n['cached']))

@contextmanager
def preserve_model(model):
    state=deepcopy(model.state_dict()); modes=[m.training for m in model.modules()]
    grads=[None if p.grad is None else p.grad.detach().clone() for p in model.parameters()]
    rng=capture_rng()
    try: yield
    finally:
        model.load_state_dict(state)
        for m,mode in zip(model.modules(),modes): m.training=mode
        for p,g in zip(model.parameters(),grads): p.grad=g
        restore_rng(rng)

def identical(a,b):
    if isinstance(a,torch.Tensor): return isinstance(b,torch.Tensor) and torch.equal(a,b)
    if isinstance(a,dict): return isinstance(b,dict) and a.keys()==b.keys() and all(identical(a[k],b[k]) for k in a)
    if isinstance(a,(list,tuple)): return type(a)==type(b) and len(a)==len(b) and all(identical(x,y) for x,y in zip(a,b))
    return a==b

def write_json(out,name,value):
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    (out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')

def init(seed=42):
    torch.set_num_threads(1); torch.manual_seed(seed); random.seed(seed); np.random.seed(seed)
