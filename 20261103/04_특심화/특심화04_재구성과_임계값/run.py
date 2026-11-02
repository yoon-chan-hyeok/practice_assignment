"""제공 실행기. 학습 대상은 tasks.py이며 이전 실습 파일은 필요 없다."""
from pathlib import Path
import json
import torch
from torch import nn
from support import init,write_json
from tasks import *
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'outputs'
OUT.mkdir(exist_ok=True)
init()

import argparse,hashlib,pandas as pd
from models import Autoencoder
parser=argparse.ArgumentParser();parser.add_argument('--evaluate-test',action='store_true');args=parser.parse_args()
features=['x'+str(i) for i in range(8)]
# CSV의 실제 feature 이름을 읽되 test 내용은 이 지점에서 읽지 않는다.
train=pd.read_csv(ROOT/'data/anomaly_train.csv');valid=pd.read_csv(ROOT/'data/anomaly_valid.csv')
features=[c for c in train.columns if c.startswith('f') or c.startswith('x')]
if len(features)!=8: features=[c for c in train.columns if c not in ['id','anomaly']]
if args.evaluate_test:
    plan=json.loads((OUT/'threshold_plan.json').read_text())
    for split in ['train','valid']:
        assert hashlib.sha256((ROOT/f'data/anomaly_{split}.csv').read_bytes()).hexdigest()==plan[split+'_sha256']
    assert hashlib.sha256((OUT/'model.pt').read_bytes()).hexdigest()==plan['model_sha256']
    # 이미 평가한 같은 버전은 저장된 결과만 읽는다. 후보를 다시 선택하지 않는다.
    if (OUT/'test_metrics.json').exists():
        recorded=json.loads((OUT/'test_metrics.json').read_text())
        if recorded['plan_sha256']!=hashlib.sha256((OUT/'threshold_plan.json').read_bytes()).hexdigest():
            raise ValueError('이미 test를 본 뒤 계획이 변경되었습니다. 새 test 없이는 다시 선택하지 않습니다.')
        print('동일 동결 버전의 기존 결과');print((OUT/'test_metrics.json').read_text());raise SystemExit(0)
    model=Autoencoder(8,2);model.load_state_dict(torch.load(OUT/'model.pt',weights_only=True));model.eval()
    test=pd.read_csv(ROOT/'data/anomaly_test.csv');x=torch.tensor(test[features].values,dtype=torch.float32)
    with torch.inference_mode(): errors=(model(x)-x).square().mean(1)
    actual=torch.tensor(test['anomaly'].values);pred=errors>plan['threshold']
    tp=int((pred&(actual==1)).sum());fp=int((pred&(actual==0)).sum());fn=int((~pred&(actual==1)).sum())
    row={'n':len(test),'tp':tp,'fp':fp,'fn':fn,'f1':2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.,
         'threshold':plan['threshold'],'plan_sha256':hashlib.sha256((OUT/'threshold_plan.json').read_bytes()).hexdigest()}
    write_json(OUT,'test_metrics.json',row);print(json.dumps(row,sort_keys=True));raise SystemExit(0)
# 기존 test 결과가 있으면 새 후보 선택을 막는다. 다른 독립 데이터가 필요함을 알린다.
if (OUT/'test_metrics.json').exists():
    print('test 평가 완료: 기존 계획을 사용하세요. 같은 test로 후보를 다시 고르지 않습니다.');raise SystemExit(0)
x=torch.tensor(train[features].values,dtype=torch.float32);v=torch.tensor(valid[features].values,dtype=torch.float32)
assert set(train['anomaly'].unique())=={0}
model=Autoencoder(8,2);optimizer=torch.optim.Adam(model.parameters(),lr=.03)
for _ in range(80):
    optimizer.zero_grad(set_to_none=True)
    loss=masked_mse(model(x).unsqueeze(1),x.unsqueeze(1),torch.zeros(len(x),1,dtype=torch.bool))
    loss.backward();optimizer.step()
model.eval()
with torch.inference_mode():errors=(model(v)-v).square().mean(1)
best,candidates=choose_threshold(errors,torch.tensor(valid['anomaly'].values))
pd.DataFrame(candidates).to_csv(OUT/'threshold_candidates.csv',index=False)
torch.save(model.state_dict(),OUT/'model.pt')
plan=dict(best,features=features,source='normal_train / labeled_valid',test_used=False,
          train_sha256=hashlib.sha256((ROOT/'data/anomaly_train.csv').read_bytes()).hexdigest(),
          valid_sha256=hashlib.sha256((ROOT/'data/anomaly_valid.csv').read_bytes()).hexdigest(),
          model_sha256=hashlib.sha256((OUT/'model.pt').read_bytes()).hexdigest())
write_json(OUT,'threshold_plan.json',plan)
print('정상 train:',len(train),'valid:',len(valid),'후보 수:',len(candidates))
print('선택 threshold/F1:',round(best['threshold'],6),round(best['f1'],6),'test 미사용')
