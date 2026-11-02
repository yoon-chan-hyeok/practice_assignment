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

from torch.nn.utils.rnn import pad_sequence,pack_padded_sequence,pad_packed_sequence
seq=[torch.arange(n*3,dtype=torch.float32).reshape(n,3) for n in [4,2,5]]
lengths=torch.tensor([4,2,5]); padded=pad_sequence(seq,batch_first=True)
# TODO D01: 정렬되지 않은 길이 [4,2,5]를 그대로 pack한다.
# lengths는 CPU의 양수 정수이다. enforce_sorted=False로 내부 정렬을 허용한다.
# BEGIN D01
packed=pack_padded_sequence(padded,lengths,batch_first=True)
# END D01
restored,restored_lengths=pad_packed_sequence(packed,batch_first=True)
print("packed data:",tuple(packed.data.shape),"batch_sizes:",packed.batch_sizes.tolist())
print("복원:",tuple(restored.shape),restored_lengths.tolist())
print("원본 일치:",torch.equal(restored,padded))
