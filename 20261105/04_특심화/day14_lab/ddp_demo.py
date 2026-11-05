"""선택 시연: CPU Gloo 2개 프로세스의 가중 CE gradient가 전체 batch와 같은지 검사.
실제 다중 GPU/AMP 재현 검증이 아닙니다. Windows 방화벽·Gloo 지원에 따라 별도 점검이 필요합니다.
"""
import tempfile,copy,json
from pathlib import Path
import torch
from torch import nn
import torch.distributed as dist
import torch.multiprocessing as mp
from torch.nn.parallel import DistributedDataParallel as DDP


def worker(rank,world,url):
    torch.set_num_threads(1);dist.init_process_group('gloo',init_method=url,rank=rank,world_size=world)
    try:
        torch.manual_seed(14);model=nn.Linear(4,3);reference=copy.deepcopy(model)
        x=torch.randn(8,4);y=torch.tensor([0,0,0,0,0,1,2,2]);weights=torch.tensor([.3,.9,1.8])
        nn.functional.cross_entropy(reference(x),y,weight=weights).backward()
        expected=[p.grad.clone() for p in reference.parameters()]
        ddp=DDP(model);ix=torch.arange(rank*4,(rank+1)*4);local_y=y[ix]
        denominator=weights[local_y].sum();dist.all_reduce(denominator)
        # DDP가 gradient를 world로 평균하므로 로컬 분자에 world/global_den을 곱한다.
        local_sum=nn.functional.cross_entropy(ddp(x[ix]),local_y,weight=weights,reduction='sum')
        (local_sum*world/denominator).backward()
        error=max((p.grad-e).abs().max().item() for p,e in zip(model.parameters(),expected))
        if error>1e-6:raise AssertionError(f'DDP gradient mismatch: {error}')
        if rank==0:print(json.dumps({'cpu_gloo_world':world,'weighted_gradient_match':True,'max_error':error},sort_keys=True),flush=True)
    finally:dist.destroy_process_group()


def main():
    if not dist.is_gloo_available():raise RuntimeError('Gloo backend unavailable')
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp)/'rendezvous';url=path.resolve().as_uri()
        mp.spawn(worker,args=(2,url),nprocs=2,join=True)

if __name__=='__main__':main()
