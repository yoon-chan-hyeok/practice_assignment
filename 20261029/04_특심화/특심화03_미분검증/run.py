from pathlib import Path
import torch, json
from tasks import analytic_mse, central_difference
X=torch.tensor([[1.,2.],[2.,-1.],[0.,3.]],dtype=torch.float64)
y=torch.tensor([2.,1.,3.],dtype=torch.float64)
w=torch.tensor([0.5,-0.25],dtype=torch.float64,requires_grad=True)
b=torch.tensor(0.2,dtype=torch.float64,requires_grad=True)
loss,gw,gb=analytic_mse(X,y,w,b)
reference=((X@w+b-y)**2).mean(); reference.backward()
num=central_difference(lambda q: ((X@q+b.detach()-y)**2).mean(),w)
result={"loss":loss.item(),"analytic_w":gw.detach().tolist(),"analytic_b":gb.item(),"autograd_w":w.grad.tolist(),"numeric_w":num.tolist(),"autograd_max_error":(gw-w.grad).abs().max().item(),"numerical_max_error":(gw-num).abs().max().item()}
out=Path(__file__).resolve().parent/"outputs";out.mkdir(exist_ok=True)
(out/"gradient_check.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,indent=2))
