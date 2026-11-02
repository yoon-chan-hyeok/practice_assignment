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

ref=nn.RNN(3,4,batch_first=True).double();cell=nn.RNNCell(3,4).double()
copy_rnn_weights(ref,cell)
x=torch.randn(2,5,3,dtype=torch.float64,requires_grad=True);x2=x.detach().clone().requires_grad_()
h=torch.randn(2,4,dtype=torch.float64,requires_grad=True);h2=h.detach().clone().requires_grad_()
a,ha=ref(x,h.unsqueeze(0));b,hb=unroll_rnn(cell,x2,h2)
(a.square().sum()+ha.sum()).backward();(b.square().sum()+hb.sum()).backward()
output_error=float((a-b).detach().abs().max());gradient_error=float((x.grad-x2.grad).abs().max())
for n,p in cell.named_parameters():torch.testing.assert_close(p.grad,getattr(ref,n+'_l0').grad,atol=1e-9,rtol=1e-7)
torch.testing.assert_close(a,b,atol=1e-9,rtol=1e-7);torch.testing.assert_close(h.grad,h2.grad,atol=1e-9,rtol=1e-7)
result={'output_shape':list(a.shape),'last_state_shape':list(hb.shape),'output_max_error':output_error,
        'input_gradient_max_error':gradient_error,'parameter_gradients_equal':True}
write_json(OUT,'rnn_check.json',result);print(json.dumps(result,sort_keys=True))
