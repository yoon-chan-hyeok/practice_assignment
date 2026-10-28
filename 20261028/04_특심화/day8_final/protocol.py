"""제공 코드: 평가 계획·동결 파일의 변경 감지. 교육용 절차 통제이며 보안 장치가 아닙니다."""
from pathlib import Path
import json,hashlib,importlib.metadata,platform
import numpy as np
from data_io import FEATURES,DERIVED,sha256,save_json
from preprocessing import candidates,CANDIDATE_ORDER

CRITICAL_FILES=['data_io.py','feature_ops.py','preprocessing.py','evaluate.py','clustering.py','protocol.py','main.py']
DEV_FILES=['cv_comparison.csv','cv_scores.csv','feature_comparison.csv','cluster_profile.csv',
           'cluster_scores.csv','cluster_assignments.csv','regression_cv.csv','fold_statistics.csv','fold_ids.csv']

def normalize(x):
    if isinstance(x,dict):return {str(k):normalize(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [normalize(v) for v in x]
    if isinstance(x,np.generic):return normalize(x.item())
    if isinstance(x,float) and not np.isfinite(x):return '__'+str(x)+'__'  # 설정의 결측 표식
    if isinstance(x,type) or callable(x):return x.__module__+'.'+x.__qualname__
    return x

def canonical(value):return json.dumps(normalize(value),ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
def digest(value):return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()
def read_json(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def write_json(path,value):save_json(path,normalize(value))
def versions():return {'python':platform.python_version(),**{n:importlib.metadata.version(n) for n in ['numpy','pandas','scipy','scikit-learn','xgboost','joblib']}}

def registry():
    """모델뿐 아니라 수치·범주 전처리의 매개변수도 기록합니다."""
    result={}
    for name,pipe in candidates().items():
        steps=[]
        for tag,chain,cols in pipe['pre'].transformers:
            steps.append({'name':tag,'columns':cols,'steps':[{'name':n,'class':type(e).__module__+'.'+type(e).__name__,'params':normalize(e.get_params(deep=False))} for n,e in chain.steps]})
        result[name]={'model_class':type(pipe['model']).__module__+'.'+type(pipe['model']).__name__,
            'params':normalize(pipe['model'].get_params(deep=False)),'preprocessing':steps,
            'engineered':'features' in pipe.named_steps}
    return result

def new_plan(dev,root):
    root=Path(root)
    return {'schema_version':1,'task':'request_failure_before_execution','positive_label':1,
        'features':FEATURES,'candidate_order':CANDIDATE_ORDER,'registry':registry(),
        'selection':'train60 StratifiedKFold5 seed42 mean F1 max; exact tie: declared order',
        'threshold':.5,'threshold_tuned':False,'decision_rule':'score > threshold; equality -> 0',
        'feature_recipe':'v1 log1p(input_chars); input_chars/(1+allowed_tools); keep NaN',
        'valid_usage':'diagnostic only, then refit after freeze',
        'train_ids':dev.X_train.index.tolist(),'valid_ids':dev.X_valid.index.tolist(),'heldout_ids':dev.test_ids,
        'data_hashes':dev.source_hashes,'code_hashes':{n:sha256(root/n) for n in CRITICAL_FILES},
        'versions':versions(),'test_policy':'freeze -> fresh refit80 -> test20; no adaptive reselection',
        'educational_notice':'test 결과는 PPT에 공개됨. 본 실습은 교육용 재현이며 새로운 독립 연구 성능이 아님'}

def verify_plan(plan,dev,root):
    current=new_plan(dev,root)
    if canonical(plan)!=canonical(current):
        changed=[k for k in current if canonical(current[k])!=canonical(plan.get(k))]
        raise ValueError(f'사전 계획 이후 코드/데이터/환경/설정 변경: {changed}')
    if (len(plan['train_ids']),len(plan['valid_ids']),len(plan['heldout_ids']))!=(60,20,20):raise ValueError('수업 분할은60/20/20입니다.')

def freeze(plan,selected,out):
    out=Path(out)
    p={**plan,'selected':selected,'derived_features':DERIVED if selected=='Logistic_FE' else [],
       'selected_params':plan['registry'][selected],'refit_ids':plan['train_ids']+plan['valid_ids'],
       'refit_n':80,'heldout_n':20,'development_outputs':{n:sha256(out/n) for n in DEV_FILES}}
    path=out/'evaluation_lock.json'
    if path.exists():
        old=read_json(path)
        if canonical(old)!=canonical(p):raise ValueError('기존 동결 설정과 다릅니다. 기존 최종 평가를 덮어쓰지 마세요.')
        return old
    write_json(path,p);(out/'evaluation_lock.sha256').write_text(digest(p)+'\n',encoding='utf-8')
    return p

def verify_lock(out,dev,root):
    out=Path(out);p=read_json(out/'evaluation_lock.json')
    if digest(p)!=(out/'evaluation_lock.sha256').read_text(encoding='utf-8').strip():raise ValueError('동결 파일 해시 변경')
    plan=read_json(out/'experiment_plan.json');verify_plan(plan,dev,root)
    if any(canonical(p.get(k))!=canonical(v) for k,v in plan.items()):raise ValueError('동결 설정과 사전 계획 불일치')
    if p['selected'] not in CANDIDATE_ORDER or p['selected_params']!=registry()[p['selected']]:raise ValueError('모델 설정 변경')
    if p['refit_ids']!=plan['train_ids']+plan['valid_ids']:raise ValueError('재학습 ID 변경')
    if any(sha256(out/n)!=h for n,h in p['development_outputs'].items()):raise ValueError('동결 후 개발 실험표 변경')
    if (out/'evaluation_receipt.json').exists() and read_json(out/'evaluation_receipt.json')['lock_sha256']!=digest(p):raise ValueError('최종 평가와 설정 해시 불일치')
    return p
