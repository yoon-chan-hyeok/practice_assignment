import argparse
import pandas as pd
import torch
from torch.utils.data import DataLoader
from tasks import benchmark,profile_steps,summarize_times
from support import seed_all,ROOT,image_dataset,small_model,save_json

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--profile',action='store_true')
    args=parser.parse_args();seed_all()
    ds=image_dataset('train');loader=DataLoader(ds,batch_size=16,shuffle=False,num_workers=0)
    batches=list(loader);model=small_model();out=ROOT/'outputs';out.mkdir(exist_ok=True)
    rows=[];summaries=[]
    for device in ('cpu','cuda'):
        for layout in (False,True):
            result=benchmark(model,batches,torch.device(device),repeats=3,warmup=1,channels_last=layout)
            rows.extend(result['rows']);print(device,'channels_last=',layout,result['status'])
            if result['rows']: summaries.append(dict(device=device,layout=layout,**summarize_times(result['rows'])))
    pd.DataFrame(rows).to_csv(out/'compute_benchmark.csv',index=False)
    save_json('timing_summary.json',summaries)
    if args.profile:
        report=profile_steps(model,loader,torch.device('cpu'),out/'trace.json')
        save_json('profile_report.json',report)
        print('별도 CPU trace 생성. profiler overhead를 포함하므로 benchmark 시간과 섞지 않는다.')
    print('원본 모델/RNG 보존, CUDA 미가용은 SKIP; 시간은 실행마다 달라진다.')
if __name__=='__main__': main()
