from pathlib import Path
import torch,json,copy
from torch.utils.data import DataLoader,TensorDataset
from tasks import train_one_epoch,evaluate
torch.set_num_threads(1);torch.manual_seed(42)
X=torch.tensor([[1.,2.],[-1.,0.],[2.,1.],[0.,0.],[1.,-1.],[-2.,1.],[3.,2.]])
y=torch.tensor([1,0,1,0,1,0,1])
loader=DataLoader(TensorDataset(X,y),batch_size=3,shuffle=False)
model=torch.nn.Sequential(torch.nn.Linear(2,8),torch.nn.ReLU(),torch.nn.Linear(8,2))
opt=torch.optim.SGD(model.parameters(),lr=0.1)
train=train_one_epoch(model,loader,opt,torch.device("cpu"))
before=copy.deepcopy(model.state_dict());grads=[p.grad.clone() for p in model.parameters()]
mode=model.training
valid=evaluate(model,loader,torch.device("cpu"))
result={"train":train,"evaluation":{k:valid[k] for k in ['loss','accuracy','samples','batches']},"weights_preserved":all(torch.equal(v,before[k]) for k,v in model.state_dict().items()),"gradients_preserved":all(torch.equal(p.grad,g) for p,g in zip(model.parameters(),grads)),"mode_preserved":model.training==mode}
out=Path(__file__).resolve().parent/"outputs";out.mkdir(exist_ok=True)
(out/"engine_contract.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,indent=2))
