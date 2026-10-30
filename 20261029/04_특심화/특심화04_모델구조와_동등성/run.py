from pathlib import Path
import torch,json
from torch import nn
from tasks import SimpleANN, copy_from_sequential
torch.manual_seed(42)
seq=nn.Sequential(nn.Linear(2,8),nn.ReLU(),nn.Linear(8,2)).double()
model=SimpleANN().double();copy_from_sequential(model,seq)
x=torch.tensor([[1.,2.],[-1.,0.]],dtype=torch.float64,requires_grad=True)
x2=x.detach().clone().requires_grad_(True)
a,b=seq(x),model(x2);a.sum().backward();b.sum().backward()
result={"parameters":sum(p.numel() for p in model.parameters()),"output_shape":list(b.shape),"same_logits":torch.allclose(a,b),"same_input_grad":torch.allclose(x.grad,x2.grad),"independent_parameters":all(p.data_ptr()!=q.data_ptr() for p,q in zip(seq.parameters(),model.parameters()))}
out=Path(__file__).resolve().parent/"outputs";out.mkdir(exist_ok=True)
(out/"model_contract.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,indent=2))
