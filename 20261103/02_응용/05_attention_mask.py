import torch
from torch import nn
torch.set_num_threads(1)  # 작은 CPU 실습의 실행 조건을 고정한다.
torch.manual_seed(42)
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"outputs"
OUT.mkdir(exist_ok=True)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
x=torch.randn(2,5,16); lengths=torch.tensor([3,5])
mask=torch.arange(5).unsqueeze(0)>=lengths.unsqueeze(1)
x[mask]=0
attention=nn.MultiheadAttention(16,4,dropout=0,batch_first=True).eval()
with torch.inference_mode():
    plain,_=attention(x,x,x)
    # TODO A05: Padding을 key로 보지 않게 bool Mask를 전달한다.
    # nn.MultiheadAttention의 key_padding_mask: [B,T], True가 제외 위치이다.
    # BEGIN A05
    masked,weights=attention(x,x,x,average_attn_weights=False)
    # END A05
    # key Mask만으로 padded query의 출력이 0이 되지는 않는다. 집계 때 다시 제외한다.
    mean=(masked*(~mask).unsqueeze(-1)).sum(1)/lengths.unsqueeze(-1)
print("shape:",tuple(masked.shape),tuple(weights.shape))
print("막은 key weight 최대:",round(weights[0,:,:,3:].abs().max().item(),6))
print("유효 query 출력 변화:",round((plain[0,:3]-masked[0,:3]).abs().max().item(),6))
print("masked mean:",tuple(mean.shape))
plt.figure(figsize=(6,3)); plt.imshow(mask.int().numpy(),vmin=0,vmax=1)
plt.xlabel("Time"); plt.ylabel("Sample"); plt.title("Padding mask: 1 = ignored")
plt.xticks(range(5)); plt.yticks(range(2)); plt.tight_layout()
plt.savefig(OUT/"mask_or_latent.png",dpi=120); plt.close()
