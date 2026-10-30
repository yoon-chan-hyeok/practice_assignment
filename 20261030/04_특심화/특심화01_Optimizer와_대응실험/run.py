from pathlib import Path
import json
import torch
import pandas as pd
BASE=Path(__file__).resolve().parent
OUT=BASE/'outputs';OUT.mkdir(exist_ok=True)
torch.set_num_threads(1)

from support import fit_fixed
from tasks import make_optimizer,summarize_runs
rows=[]
for seed in (41,42,43):
    for setting in ('sgd','adamw'):
        config=dict(seed=seed,optimizer=setting,lr=.01,weight_decay=0.,width=32,batch_size=32,epochs=20)
        model,history,trace=fit_fixed(config,optimizer_factory=make_optimizer)
        history.to_csv(OUT/f'{setting}_{seed}_history.csv',index=False)
        rows.append(dict(setting=setting,seed=seed,best_valid_loss=float(history.valid_loss.min())))
raw=pd.DataFrame(rows);summary=summarize_runs(rows)
raw.to_csv(OUT/'raw_runs.csv',index=False);summary.to_csv(OUT/'paired_summary.csv',index=False)
print(summary.round(6).to_string(index=False))
print('조건: 같은 seed·초기화·shuffle·20 epochs / test 미사용 / 우열의 통계적 증명 아님')
