import torch
from torch import nn
torch.set_num_threads(1)  # 작은 CPU 실습의 실행 조건을 고정한다.
torch.manual_seed(42)
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"outputs"
OUT.mkdir(exist_ok=True)

from torch.nn.utils.rnn import pad_sequence
sequences=[torch.ones(4,3),torch.ones(2,3)*2,torch.ones(5,3)*3]
lengths=torch.tensor([4,2,5]); padded=pad_sequence(sequences,batch_first=True)
mask=torch.arange(padded.size(1)).unsqueeze(0)>=lengths.unsqueeze(1)
# TODO A01: Padding이 아닌 실제 시점만 합산하고 각 자료의 실제 길이로 나눈다.
# mask=True는 Padding이다. 0도 정상 관측값일 수 있으므로 값이 0인지로 판정하지 않는다.
# BEGIN A01
mean=padded.mean(dim=1)
# END A01
print("Padding mask:\n",mask)
print("실제 값 평균:\n",mean)
pd.DataFrame(mask.int().numpy()).to_csv(OUT/"padding_mask.csv",index=False)
