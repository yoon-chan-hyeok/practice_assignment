import torch
import pandas as pd
from tasks import trace_leaves,summarize_trace
from support import seed_all,small_model,save_json,ROOT

def main():
    seed_all();model=small_model(batchnorm=True,dropout=0.2).train();x=torch.rand(4,3,32,32)
    rows=trace_leaves(model,x);summary=summarize_trace(rows)
    out=ROOT/'outputs';out.mkdir(exist_ok=True)
    pd.DataFrame(rows).to_csv(out/'layer_trace.csv',index=False);save_json('trace_summary.json',summary)
    print(pd.DataFrame(rows)[['name','call','shape','parameters']].to_string(index=False))
    print('hook 제거/상태 복원 후 재실행 결과:',len(trace_leaves(model,x)),'행')
if __name__=='__main__': main()
