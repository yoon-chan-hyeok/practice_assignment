from pathlib import Path
import json
import torch
import pandas as pd
BASE=Path(__file__).resolve().parent
OUT=BASE/'outputs';OUT.mkdir(exist_ok=True)
torch.set_num_threads(1)

from support import fit_fixed,load_data
from tasks import mc_predict
model,history,_=fit_fixed(dict(seed=42,width=16,norm='batch',dropout=.3,epochs=20,lr=.01))
_,_,Xv,yv,ids,_=load_data()
model.eval()
with torch.no_grad(): standard=model(Xv).softmax(1).cpu()
result=mc_predict(model,Xv,repeats=30,seed=123)
repeat=mc_predict(model,Xv,repeats=30,seed=123)
table=pd.DataFrame({'id':ids['valid'],'actual':yv.tolist(),'eval_p1':standard[:,1].tolist(),
                    'mc_mean_p1':result['mean'][:,1].tolist(),'mc_variance_p1':result['variance'][:,1].tolist()})
table.to_csv(OUT/'mc_predictions.csv',index=False)
report={'repeats':30,'same_seed_equal':torch.equal(result['mean'],repeat['mean']),
        'mean_probability_variance':float(result['variance'].mean()),'test_used':False,
        'scope':'Exploratory prediction variability; not a calibrated risk.'}
(OUT/'mc_report.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report,indent=2))
