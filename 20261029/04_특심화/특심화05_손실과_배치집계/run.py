from pathlib import Path
import json, torch
from tasks import stable_cross_entropy, weighted_batch_mean
x=torch.tensor([[1000.,-1000.],[-1000.,1000.]],dtype=torch.float64,requires_grad=True)
y=torch.tensor([1,1])
a=stable_cross_entropy(x,y);a.backward()
ref=torch.nn.functional.cross_entropy(x.detach(),y)
result={"loss":a.item(),"reference":ref.item(),"finite":bool(torch.isfinite(a)),"gradient":x.grad.tolist(),"weighted_mean":weighted_batch_mean([(0.1,4),(0.2,4),(0.9,2)])}
out=Path(__file__).resolve().parent/"outputs";out.mkdir(exist_ok=True)
(out/"loss_contract.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,indent=2))
