from pathlib import Path
import json
import torch
import pandas as pd
BASE=Path(__file__).resolve().parent
OUT=BASE/'outputs';OUT.mkdir(exist_ok=True)
torch.set_num_threads(1)

from support import fit_fixed
from tasks import make_scheduler,advance_scheduler
rows=[]
for kind in ('plateau','cosine'):
    _,history,_=fit_fixed(dict(seed=42,lr=.01,width=32,epochs=30,scheduler=kind),
        scheduler_factory=make_scheduler,scheduler_step=advance_scheduler)
    history.to_csv(OUT/f'{kind}_history.csv',index=False)
    changes=history.loc[history.lr_used!=history.lr_next,'epoch'].tolist()
    rows.append(dict(scheduler=kind,best_valid_loss=float(history.valid_loss.min()),
                     changed_at_epoch=changes,first_lr=float(history.iloc[0].lr_used),last_next_lr=float(history.iloc[-1].lr_next)))
(OUT/'scheduler_report.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
print(json.dumps(rows,indent=2))
