import copy
import torch
from torch.utils.data import TensorDataset,DataLoader
from tasks import accumulated_step,evaluate
from support import seed_all,small_model,synthetic,save_json

def main():
    seed_all();x,y=synthetic(10);base=small_model().eval();one=copy.deepcopy(base);micro=copy.deepcopy(base)
    a=torch.optim.SGD(one.parameters(),lr=0.01);b=torch.optim.SGD(micro.parameters(),lr=0.01)
    full=accumulated_step(one,a,[(x,y)],torch.device('cpu'),torch.amp.GradScaler('cuda',enabled=False),1.0)
    partial=accumulated_step(micro,b,[(x[:3],y[:3]),(x[3:8],y[3:8]),(x[8:],y[8:])],torch.device('cpu'),torch.amp.GradScaler('cuda',enabled=False),1.0)
    for p,q in zip(one.parameters(),micro.parameters()): torch.testing.assert_close(p,q,atol=1e-6,rtol=1e-5)
    result=evaluate(micro,DataLoader(TensorDataset(x,y),batch_size=4),torch.device('cpu'))
    delta=max(float((p-q).detach().abs().max()) for p,q in zip(one.parameters(),micro.parameters()))
    save_json('accumulation.json',dict(full=full,micro=partial,evaluation=result,parameter_max_abs=delta))
    print('큰 배치 10 vs micro 3/5/2:',partial['samples'],'표본 / 갱신 동등성 통과')
    print('평가 표본:',result['samples'],'AMP:',partial['amp_active'],'CPU에서는 FP32')
if __name__=='__main__': main()
