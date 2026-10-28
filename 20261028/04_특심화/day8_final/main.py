"""Day8 최종 프로젝트. 첫 실행: 개발→동결→80건 재학습→test 평가.
같은 코드의 재실행은 동결 버전의 재현성 확인이며 모델을 다시 고르지 않습니다.
"""
from pathlib import Path
import os
os.environ.setdefault('OMP_NUM_THREADS','1')
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import argparse
import numpy as np
import pandas as pd
from data_io import load_data,read_table,save_table,save_json,FEATURES,check_features,classification_folds,sha256
from evaluate import compare_candidates,choose_candidate,refit_development,classification_metrics,regression_cv,fold_statistics
from preprocessing import failure_scores
from clustering import cluster_analysis
from protocol import new_plan,verify_plan,freeze,verify_lock,write_json,read_json,digest
ROOT=Path(__file__).resolve().parent

def develop(out):
    """후보 비교 전 계획부터 저장합니다. test 입력/정답은 아직 선택하지 않습니다."""
    if (out/'evaluation_lock.json').exists():raise ValueError('이미 동결됨: develop 대신 reproduce를 사용하세요.')
    dev=load_data(ROOT/'data');write_json(out/'experiment_plan.json',new_plan(dev,ROOT))
    table,detail=compare_candidates(dev)
    save_table(out/'cv_comparison.csv',table);save_table(out/'cv_scores.csv',detail)
    save_table(out/'feature_comparison.csv',table[table.model.isin(['Logistic','Logistic_FE'])])
    profile,scores,assignments=cluster_analysis(dev.X_train)
    save_table(out/'cluster_profile.csv',profile);save_table(out/'cluster_scores.csv',scores)
    save_table(out/'cluster_assignments.csv',assignments);save_table(out/'regression_cv.csv',regression_cv(dev))
    save_table(out/'fold_statistics.csv',fold_statistics(dev))
    fold_ids=[]
    for j,(a,b) in enumerate(classification_folds(dev),1):
        for part,positions in [('fit',a),('evaluate',b)]:
            fold_ids.extend({'fold':j,'part':part,'position':i,'request_id':dev.X_train.index[pos]} for i,pos in enumerate(positions))
    save_table(out/'fold_ids.csv',pd.DataFrame(fold_ids))
    selected=choose_candidate(table)
    write_json(out/'selection.json',{'selected':selected,'table_sha256':sha256(out/'cv_comparison.csv')})
    print('개발 완료: 7후보 CV·특성 비교·군집·회귀 CV·fold 통계 / test 미사용')
    return table

def freeze_stage(out):
    dev=load_data(ROOT/'data')
    if (out/'evaluation_lock.json').exists():return verify_lock(out,dev,ROOT)
    plan=read_json(out/'experiment_plan.json');verify_plan(plan,dev,ROOT)
    selected=read_json(out/'selection.json')
    if sha256(out/'cv_comparison.csv')!=selected['table_sha256']:raise ValueError('선택 이후 실험표 변경')
    table=pd.read_csv(out/'cv_comparison.csv',float_precision='round_trip')
    if choose_candidate(table)!=selected['selected']:raise ValueError('선택 규칙과 실험표 불일치')
    p=freeze(plan,selected['selected'],out)
    print('설정 동결:',p['selected'],'/ threshold=0.5, strict > / 개발80건 재학습 허용')
    return p

def heldout_after_freeze(out,dev):
    """동결 검사를 통과한 뒤에만 test의 X/y를 가져옵니다."""
    p=verify_lock(out,dev,ROOT)
    raw=read_table(ROOT/'data/requests.csv').set_index('request_id')
    X=check_features(raw.loc[p['heldout_ids'],FEATURES]);y=raw.loc[p['heldout_ids'],'failed']
    return X,y

def fitted_snapshot(pipe):
    pre=pipe['pre'];num=pre.named_transformers_['num'];cat=pre.named_transformers_['cat']
    result={'median':num['imputer'].statistics_.tolist(),'mode':cat['imputer'].statistics_.tolist(),
            'categories':[v.tolist() for v in cat['encoder'].categories_]}
    if 'scaler' in num.named_steps:result.update(mean=num['scaler'].mean_.tolist(),scale=num['scaler'].scale_.tolist())
    return result

def evaluate_stage(out,reproduce=False,save_model=False):
    dev=load_data(ROOT/'data');p=verify_lock(out,dev,ROOT)
    final=refit_development(p,dev);before=fitted_snapshot(final)
    X,y=heldout_after_freeze(out,dev)
    probability=failure_scores(final,X);pred=(probability>p['threshold']).astype(int)
    if before!=fitted_snapshot(final):raise AssertionError('predict가 학습 통계를 바꾸었습니다.')
    report=classification_metrics(y,pred,probability)
    report.update(scope='frozen_test20',model=p['selected'],positive_label=1,threshold=p['threshold'],decision_rule=p['decision_rule'])
    frame=pd.DataFrame({'request_id':X.index,'actual':y.to_numpy(),'probability_failed':probability,'predicted':pred})
    receipt=out/'evaluation_receipt.json'
    if reproduce or receipt.exists():
        if not receipt.exists():raise ValueError('재현할 최종 평가가 없습니다.')
        old=pd.read_csv(out/'test_predictions.csv');previous=read_json(out/'test_metrics.json')
        if old.request_id.tolist()!=frame.request_id.tolist() or not np.array_equal(old.predicted,pred) or not np.allclose(old.probability_failed,probability,rtol=1e-10,atol=1e-12):raise AssertionError('재현 확률/예측 불일치')
        if any(not np.isclose(report[k],previous[k],rtol=1e-10,atol=1e-12) for k in ['Accuracy','Precision','Recall','F1','ROC_AUC','TN','FP','FN','TP']):raise AssertionError('재현 지표 불일치')
        save_json(out/'reproduction_check.json',{'same_lock':True,'same_probabilities':True,'same_predictions':True,'same_metrics':True,'reselection':False})
        print('동결 버전 재현: 확률·예측·지표 일치 / 재선택 없음')
    else:
        save_json(out/'test_metrics.json',report);save_table(out/'test_predictions.csv',frame)
        save_json(out/'refit_statistics.json',{'refit_n':80,'statistics':before})
        errors=frame[frame.actual!=frame.predicted].copy();errors['error_type']=np.where(errors.actual==1,'FN','FP')
        save_table(out/'error_cases.csv',errors)
        # 모든 결과를 저장한 다음에 평가 기록을 남깁니다. 기존 평가를 임의로 덮어쓰지 않습니다.
        save_json(receipt,{'lock_sha256':digest(p),'refit_n':80,'heldout_n':20,
            'metrics_sha256':sha256(out/'test_metrics.json'),'predictions_sha256':sha256(out/'test_predictions.csv')})
        print('최종 지표:',{k:round(report[k],6) for k in ['Accuracy','Precision','Recall','F1','ROC_AUC']})
        print('TN FP FN TP:',[report[k] for k in ['TN','FP','FN','TP']])
    if save_model:
        from persistence import save_local_model
        save_local_model(final,out,p,dev.X_valid)
    return final,report,frame

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage',choices=['all','develop','freeze','evaluate','reproduce'],default='all')
    parser.add_argument('--output',type=Path,default=ROOT/'outputs')
    parser.add_argument('--save-model',action='store_true')
    a=parser.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    if a.stage=='develop':develop(out)
    elif a.stage=='freeze':freeze_stage(out)
    elif a.stage=='evaluate':evaluate_stage(out,save_model=a.save_model)
    elif a.stage=='reproduce':evaluate_stage(out,reproduce=True,save_model=a.save_model)
    elif (out/'evaluation_receipt.json').exists():evaluate_stage(out,reproduce=True,save_model=a.save_model)
    else:
        if not (out/'evaluation_lock.json').exists():develop(out);freeze_stage(out)
        evaluate_stage(out,save_model=a.save_model)
if __name__=='__main__':main()
