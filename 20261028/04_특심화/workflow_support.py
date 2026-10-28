"""제공 코드: 실습06의 단계 제어·파일 저장.
기본필수에서는 선택/재학습 함수를 main.py에서 구현합니다.
응용·심화에서는 이미 완성한 기본 흐름을 재사용하여 오류 분석과 변경 감지에 집중합니다.
"""
from pathlib import Path
import json,hashlib,inspect
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer,f1_score,roc_auc_score
from course_support import (load_data,read_table,check_features,FEATURES,DERIVED,classification_folds,
    save_json,save_table,sha256)
from model_support import candidates,CANDIDATE_ORDER,failure_scores,classification_metrics

def compare_candidates(dev):
    """고정7후보를 train60 내부5-fold로 비교합니다. valid는 진단용입니다."""
    rows=[];details=[];folds=classification_folds(dev)
    for i,(name,pipe) in enumerate(candidates().items()):
        scores=cross_validate(pipe,dev.X_train,dev.yc_train,cv=folds,
            scoring={'f1':make_scorer(f1_score,zero_division=0),'auc':'roc_auc'},
            n_jobs=1,error_score='raise',return_train_score=True)
        fitted=clone(pipe).fit(dev.X_train,dev.yc_train)
        probability=failure_scores(fitted,dev.X_valid)
        rows.append({'model':name,'CV_F1':float(scores['test_f1'].mean()),
            'CV_std':float(scores['test_f1'].std(ddof=0)), 'CV_AUC':float(scores['test_auc'].mean()),
            'valid_F1':float(f1_score(dev.yc_valid,probability>.5,zero_division=0)),
            'valid_AUC':float(roc_auc_score(dev.yc_valid,probability)), 'tie_order':i})
        for j,(a,b) in enumerate(folds):
            details.append({'model':name,'fold':j+1,'F1':scores['test_f1'][j],
                'AUC':scores['test_auc'][j],'fit_n':len(a),'eval_n':len(b),'scope':'train60_internal_cv'})
    return pd.DataFrame(rows),pd.DataFrame(details)

def choose_reference(table):
    return str(table.sort_values(['CV_F1','tie_order'],ascending=[False,True],kind='stable').iloc[0].model)

def refit_reference(protocol,dev):
    X=pd.concat([dev.X_train,dev.X_valid]);y=pd.concat([dev.yc_train,dev.yc_valid])
    if X.index.tolist()!=protocol['refit_ids']:raise ValueError('재학습 ID 불일치')
    return clone(candidates()[protocol['selected']]).fit(X,y)

def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)

def digest(value):return hashlib.sha256(canonical(value).encode()).hexdigest()

def config_value(v):
    """XGB 설정의 missing=np.nan은 설정 표식으로 기록합니다. 성능 NaN 대체가 아닙니다."""
    if isinstance(v,dict):return {str(k):config_value(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [config_value(x) for x in v]
    if isinstance(v,np.generic):return config_value(v.item())
    if isinstance(v,float) and not np.isfinite(v):return str(v)
    return v

def mini_protocol(selected,dev):
    return {'schema_version':1,'selected':selected,'candidates':CANDIDATE_ORDER,
      'features':FEATURES,'derived_features':DERIVED if selected=='Logistic_FE' else [],
      'feature_recipe':'log1p(input_chars); input_chars/(1+allowed_tools); keep NaN',
      'positive_label':1,'selection':'train60 mean 5-fold F1 max; exact tie: candidate order',
      'threshold':.5,'threshold_tuned':False,'decision_rule':'score > threshold; equality -> 0',
      'model_params':config_value(candidates()[selected]['model'].get_params(deep=False)),
      'refit_ids':dev.X_train.index.tolist()+dev.X_valid.index.tolist(),'heldout_ids':dev.test_ids,
      'data_hashes':dev.source_hashes,'test_policy':'freeze -> fresh refit80 -> test20; no adaptive reselection',
      'notice':'공개된 교육용 test 결과의 재현이며 독립 연구 성능이 아닙니다.'}

def verify_mini_lock(out,dev):
    out=Path(out);p=json.loads((out/'evaluation_lock.json').read_text(encoding='utf-8'))
    expected=(out/'evaluation_lock.sha256').read_text(encoding='utf-8').strip()
    if digest(p)!=expected:raise ValueError('동결 파일 내용이 변경되었습니다.')
    if p['selected'] not in CANDIDATE_ORDER or canonical(p)!=canonical(mini_protocol(p['selected'],dev)):
        raise ValueError('동결 후 모델/임계값/데이터 설정이 변경되었습니다.')
    return p

def run_mini(out,selector=choose_reference,refitter=refit_reference):
    """시험용 작은 흐름. 동일 동결 버전 재실행은 결과 대조만 하고 이전 최종 파일을 보존합니다."""
    out=Path(out);out.mkdir(parents=True,exist_ok=True);dev=load_data()
    lock=out/'evaluation_lock.json';receipt=out/'evaluation_receipt.json'
    if lock.exists():
        protocol=verify_mini_lock(out,dev)
    else:
        # 후보 목록과 선택 지표를 먼저 기록합니다. 아직 test의 X/y를 선택하지 않습니다.
        save_json(out/'experiment_plan.json',{'candidates':CANDIDATE_ORDER,'criterion':'mean CV F1',
            'threshold':.5,'folds':5,'train_n':60,'valid_usage':'diagnostic','test_usage':'after freeze'})
        table,details=compare_candidates(dev);selected=selector(table)
        if selected not in CANDIDATE_ORDER:raise ValueError('후보 목록에 없는 모델')
        save_table(out/'cv_comparison.csv',table);save_table(out/'cv_scores.csv',details)
        protocol=mini_protocol(selected,dev)
        save_json(lock,protocol);(out/'evaluation_lock.sha256').write_text(digest(protocol)+'\n',encoding='utf-8')
    verify_mini_lock(out,dev)
    model=refitter(protocol,dev)
    # 모델 학습이 끝난 뒤 최초로 test의 입력과 정답을 가져옵니다.
    raw=read_table(Path(__file__).resolve().parent/'data/requests.csv').set_index('request_id')
    X=check_features(raw.loc[protocol['heldout_ids'],FEATURES]);y=raw.loc[protocol['heldout_ids'],'failed']
    score=failure_scores(model,X);pred=(score>protocol['threshold']).astype(int)
    metrics=classification_metrics(y,pred,score)
    frame=pd.DataFrame({'request_id':X.index,'actual':y.to_numpy(),'probability_failed':score,'predicted':pred})
    if receipt.exists():
        old=pd.read_csv(out/'test_predictions.csv');old_metrics=json.loads((out/'test_metrics.json').read_text(encoding='utf-8'))
        if old.request_id.tolist()!=frame.request_id.tolist() or not np.array_equal(old.predicted,pred) or not np.allclose(old.probability_failed,score,rtol=1e-10,atol=1e-12):
            raise AssertionError('동일 버전의 재현 결과가 달라졌습니다.')
        if any(not np.isclose(metrics[k],old_metrics[k]) for k in metrics):raise AssertionError('재현 지표 불일치')
    else:
        save_json(out/'test_metrics.json',metrics);save_table(out/'test_predictions.csv',frame)
        save_json(receipt,{'lock_sha256':digest(protocol),'refit_n':80,'test_n':20})
    return {'protocol':protocol,'model':model,'metrics':metrics,'predictions':frame}
