"""제공 실행기. 학습 대상은 tasks.py이며 이전 실습 파일은 필요 없다."""
from pathlib import Path
import json
import torch
from torch import nn
from support import init,write_json
from tasks import *
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'outputs'
OUT.mkdir(exist_ok=True)
init()

import pandas as pd
attention=nn.MultiheadAttention(8,2,dropout=0,batch_first=True).double()
x=torch.randn(2,5,8,dtype=torch.float64,requires_grad=True)
mask=torch.tensor([[False,False,False,True,True],[False]*5])
out,pooled,weights=masked_attention(attention,x,mask,causal=True)
changed=x.detach().clone();changed[mask]=1000
_,p2,_=masked_attention(attention,changed,mask,causal=True)
torch.testing.assert_close(pooled,p2,atol=1e-9,rtol=1e-7)
pooled.square().sum().backward();assert torch.isfinite(x.grad).all()
rows=head_statistics(weights,mask);pd.DataFrame(rows).to_csv(OUT/'head_summary.csv',index=False)
result={'output_shape':list(out.shape),'weights_shape':list(weights.shape),'reported_weights_bytes':weights.numel()*weights.element_size(),
        'causal_upper_triangle_zero':bool(weights.triu(1).eq(0).all()),'padding_invariance':True}
write_json(OUT,'attention_check.json',result)
print(pd.DataFrame(rows).round(6).to_string(index=False));print(json.dumps(result,sort_keys=True))
