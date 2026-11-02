import torch
import pandas as pd
from torch import nn
from tasks import conv_cost,grouped_reference
from support import seed_all,save_json,ROOT

def main():
    seed_all();x=torch.rand(2,8,16,16,dtype=torch.float64)
    rows=[]
    for name,cout,k,p,d,g in [('normal',16,3,1,1,1),('depthwise',8,3,1,1,8),('pointwise',16,1,0,1,1),('dilated',16,3,2,2,1)]:
        layer=nn.Conv2d(8,cout,k,padding=p,dilation=d,groups=g).double()
        cost=conv_cost(tuple(x.shape),cout,k,padding=p,dilation=d,groups=g)
        expected=layer(x);actual=grouped_reference(x,layer.weight,layer.bias,padding=p,dilation=d,groups=g)
        torch.testing.assert_close(actual,expected,atol=1e-9,rtol=1e-9)
        assert tuple(expected.shape)==cost['shape'] and sum(v.numel() for v in layer.parameters())==cost['parameters']
        rows.append(dict(name=name,**cost,max_abs=float((actual-expected).detach().abs().max())))
    out=ROOT/'outputs';out.mkdir(exist_ok=True)
    pd.DataFrame(rows).to_csv(out/'conv_cost.csv',index=False)
    print(pd.DataFrame(rows)[['name','shape','parameters','macs']].to_string(index=False))
    print('MAC은 계산량 추정치이며 처리시간이 아니다.')
if __name__=='__main__': main()
