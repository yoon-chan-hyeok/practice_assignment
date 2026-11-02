import torch
from torch import nn
torch.set_num_threads(1)  # 작은 CPU 실습의 실행 조건을 고정한다.
torch.manual_seed(42)
from pathlib import Path
import sys
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"day12_sequence_models"))  # 제공 모듈의 위치; 수정하지 않는다.
OUT=Path(__file__).resolve().parent/"outputs"
OUT.mkdir(exist_ok=True)

from torch.nn.utils.rnn import pad_sequence,pack_padded_sequence
seq=[torch.randn(n,3) for n in [4,2,5]]; lengths=torch.tensor([4,2,5]); x=pad_sequence(seq,batch_first=True)
model=nn.RNN(3,8,batch_first=True).eval()
with torch.inference_mode():
    output,h_dense=model(x)
    _,h_packed=model(pack_padded_sequence(x,lengths,batch_first=True,enforce_sorted=False))
    # TODO D02: 각 자료의 실제 마지막 시점에 해당하는 output을 선택한다.
    # BEGIN D02
    last_valid=output[:,-1]
    # END D02
print("dense 마지막 vs packed:",round((h_dense[-1]-h_packed[-1]).abs().max().item(),6))
print("유효 시점 gather vs packed:",torch.allclose(last_valid,h_packed[-1],atol=1e-6))
print("단방향 RNN·eval·우측 Padding의 비교. 양방향은 단순 gather로 대체할 수 없다.")
