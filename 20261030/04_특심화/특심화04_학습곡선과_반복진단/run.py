from pathlib import Path
import json
import torch
import pandas as pd
BASE=Path(__file__).resolve().parent
OUT=BASE/'outputs';OUT.mkdir(exist_ok=True)
torch.set_num_threads(1)

from support import fit_fixed
from tasks import summarize_best,summarize_curve
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
parts=[]
for seed in (40,41,42,43,44):
    _,history,_=fit_fixed(dict(seed=seed,width=64,train_size=60,epochs=40,lr=.01))
    history.insert(0,'seed',seed);parts.append(history)
history=pd.concat(parts,ignore_index=True)
best=summarize_best(history);curve=summarize_curve(history)
history.to_csv(OUT/'raw_history.csv',index=False)
best.to_csv(OUT/'best_by_seed.csv',index=False);curve.to_csv(OUT/'curve_summary.csv',index=False)
plt.figure(figsize=(8,5))
plt.plot(curve.epoch,curve.train_mean,label='Train: mean')
plt.plot(curve.epoch,curve.valid_mean,label='Valid: mean')
plt.fill_between(curve.epoch,curve.valid_mean-curve.valid_std,curve.valid_mean+curve.valid_std,alpha=.2,label='Valid: ±1 sample SD')
plt.xlabel('Epoch');plt.ylabel('Evaluation cross-entropy');plt.legend();plt.tight_layout()
plt.savefig(OUT/'curve_variation.png',dpi=150);plt.close()
print(best.round(6).to_string(index=False))
print('평균 곡선 최저 epoch:',int(curve.loc[curve.valid_mean.idxmin(),'epoch']))
print('음영은 5개 seed의 표준편차이며 신뢰구간이 아닙니다. test 미사용.')
