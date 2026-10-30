from pathlib import Path
import torch, json
from tasks import validate_batch, move_batch
X=torch.tensor([[1.,2.],[3.,4.]],requires_grad=True)
y=torch.tensor([0,1])
before=X.detach().clone()
a,b=move_batch(X,y,torch.device("cpu")); a.sum().backward()
result={"shape":list(a.shape),"dtype":str(a.dtype),"device":str(a.device),"original_unchanged":torch.equal(X.detach(),before),"gradient":X.grad.tolist()}
out=Path(__file__).resolve().parent/"outputs";out.mkdir(exist_ok=True)
(out/"tensor_contract.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,indent=2))
