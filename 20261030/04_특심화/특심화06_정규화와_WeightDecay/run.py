from pathlib import Path
import json
import torch
import pandas as pd
BASE=Path(__file__).resolve().parent
OUT=BASE/'outputs';OUT.mkdir(exist_ok=True)
torch.set_num_threads(1)

from support import build_model,load_data
from tasks import normalization_probe,decay_groups
from torch import nn
X,_,_,_,_,_=load_data()
activation=torch.cat([X,X.square(),X.sin(),X.cos()],dim=1).float()
table=normalization_probe(activation);table.to_csv(OUT/'normalization_probe.csv',index=False)
torch.manual_seed(42)
model=build_model(dict(width=16,norm='batch'))
groups=decay_groups(model,.01)
optimizer=torch.optim.AdamW(groups,lr=.01)
report={'groups':[{'weight_decay':g['weight_decay'],'tensors':len(g['params']),
                  'parameters':sum(p.numel() for p in g['params'])} for g in groups],
        'trainable_parameters':sum(p.numel() for p in model.parameters() if p.requires_grad),
        'probe_rows':len(table),'test_used':False}
(OUT/'groups.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(table.groupby(['norm','batch_size'])[['seen','batch_mean_variance','running_mean_mse']].mean().round(6).to_string())
print(json.dumps(report,indent=2))
