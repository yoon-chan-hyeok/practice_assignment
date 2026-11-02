import argparse
import pandas as pd
import torch
from tasks import make_loader,measure_loading
from support import ROOT,image_dataset,seed_all,save_json

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--workers',type=int,default=0)
    args=parser.parse_args();seed_all();ds=image_dataset('train',with_index=True)
    loader,_=make_loader(ds,16,args.workers,True,42,torch.device('cpu'))
    rows=measure_loading(loader,2)
    fresh,_=make_loader(ds,16,args.workers,True,42,torch.device('cpu'))
    again=measure_loading(fresh,1)
    assert rows[0]['ids']==again[0]['ids']
    assert rows[0]['batch_sizes']==[16,16,16,12]
    for r in rows: r['workers']=args.workers
    out=ROOT/'outputs';out.mkdir(exist_ok=True)
    pd.DataFrame([{k:v for k,v in r.items() if k!='ids'} for r in rows]).to_csv(out/'loader_benchmark.csv',index=False)
    save_json('loader_order.json',dict(workers=args.workers,rows=rows,same_initial_order=True))
    print('workers:',args.workers,'이미지:',rows[0]['images'],'배치:',rows[0]['batch_sizes'])
    print('새 loader의 첫 epoch 순서 일치:',True,'host 로딩만 측정; GPU 대기시간 아님')
if __name__=='__main__': main()
