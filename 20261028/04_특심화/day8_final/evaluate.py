"""지표·교차검증·선택·재학습. test의 X/y는 선택 함수에 전달하지 않습니다."""
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import cross_validate
from sklearn.metrics import (confusion_matrix,accuracy_score,precision_score,recall_score,
    f1_score,roc_auc_score,make_scorer)
from data_io import NUM,DERIVED,classification_folds,regression_folds
from preprocessing import candidates,CANDIDATE_ORDER,build,failure_scores
from feature_ops import add_features

def classification_metrics(y,pred,score=None):
    """[D8-P02] 실패1 기준 네 지표·네 칸·n·positive_n·AUC를 dict로 반환합니다.
    AUC는 연속 점수로 계산합니다. 정답이 한 종류면 None을 반환합니다.
    Precision/Recall/F1의 분모0은 운영 표기0이며 표본 수로 그 상황을 알립니다.
    """
    if isinstance(y,pd.Series):
        for values in [pred,score]:
            if isinstance(values,pd.Series) and not y.index.equals(values.index):
                raise ValueError('평가 배열의 ID/순서가 다릅니다.')
    y=np.asarray(y);pred=np.asarray(pred)
    if y.ndim!=1 or len(y)==0 or pred.shape!=y.shape or not np.isin(y,[0,1]).all() or not np.isin(pred,[0,1]).all():
        raise ValueError('같은 길이의0/1 정답·예측이 필요합니다.')
    if score is not None:
        score=np.asarray(score,dtype=float)
        if score.shape!=y.shape or not np.isfinite(score).all() or (score<0).any() or (score>1).any():
            raise ValueError('실패 확률은 정답과 길이가 같은 유한한0~1 값이어야 합니다.')
    # TODO D8-P02: 함수의 계약과 README를 보고 구현하세요.
    raise NotImplementedError("TODO D8-P02")

def choose_candidate(table):
    """[D8-P03] CV_F1 최대 모델 이름을 반환합니다. 완전 동점은 사전 후보 순서입니다.
    반올림 전 수치로 비교하며 valid_F1/test 성능을 선택 기준에 추가하지 않습니다.
    """
    if set(table.model)!=set(CANDIDATE_ORDER) or table.model.duplicated().any():raise ValueError('7개 후보가 한 번씩 필요합니다.')
    if not np.isfinite(table.CV_F1).all():raise ValueError('CV_F1 계산 불가 값')
    # TODO D8-P03: 함수의 계약과 README를 보고 구현하세요.
    raise NotImplementedError("TODO D8-P03")

def refit_development(protocol,dev):
    """[D8-P04] 확정된 후보의 새 clone을 개발80건에 학습하여 반환합니다.
    X/y는 train→valid 순서로 결합합니다. 기존 valid는 이제 독립 평가 자료가 아닙니다.
    """
    X=pd.concat([dev.X_train,dev.X_valid]);y=pd.concat([dev.yc_train,dev.yc_valid])
    if X.index.tolist()!=protocol['refit_ids'] or not X.index.equals(y.index):raise ValueError('재학습 ID 불일치')
    # TODO D8-P04: 함수의 계약과 README를 보고 구현하세요.
    raise NotImplementedError("TODO D8-P04")

def compare_candidates(dev):
    """제공 코드: 앞 실습의 다중 지표 CV를7후보에 반복합니다. 전처리도 매 fold 안에서 fit."""
    rows=[];detail=[];folds=classification_folds(dev)
    for order,(name,pipe) in enumerate(candidates().items()):
        score=cross_validate(pipe,dev.X_train,dev.yc_train,cv=folds,
            scoring={'f1':make_scorer(f1_score,zero_division=0),'auc':'roc_auc'},
            return_train_score=True,n_jobs=1,error_score='raise')
        p=clone(pipe).fit(dev.X_train,dev.yc_train)
        probability=failure_scores(p,dev.X_valid)
        rows.append({'model':name,'CV_F1':float(score['test_f1'].mean()),
            'CV_std':float(score['test_f1'].std(ddof=0)),'CV_AUC':float(score['test_auc'].mean()),
            'valid_F1':float(f1_score(dev.yc_valid,probability>.5,zero_division=0)),
            'valid_AUC':float(roc_auc_score(dev.yc_valid,probability)),'tie_order':order})
        for j,(a,b) in enumerate(folds):
            detail.append({'model':name,'fold':j+1,'F1':score['test_f1'][j],'AUC':score['test_auc'][j],
                'train_F1':score['train_f1'][j],'fit_n':len(a),'eval_n':len(b),'scope':'train60_internal_cv'})
    return pd.DataFrame(rows),pd.DataFrame(detail)

def regression_cv(dev):
    """제공 코드: 실습03의 회귀 기록을 통합합니다. 최종 회귀test는 공통 필수가 아닙니다."""
    from sklearn.linear_model import LinearRegression
    from sklearn.neighbors import KNeighborsRegressor
    rows=[];folds=regression_folds(dev)
    for name,est in [('Linear',LinearRegression()),('KNN15',KNeighborsRegressor(n_neighbors=15))]:
        score=cross_validate(build(est),dev.X_train,dev.yr_train,cv=folds,
            scoring='neg_root_mean_squared_error',n_jobs=1,error_score='raise')
        rows.extend({'model':name,'fold':i,'RMSE_ms':float(v),'scope':'train60_internal_cv'} for i,v in enumerate(-score['test_score'],1))
    return pd.DataFrame(rows)

def fold_statistics(dev):
    """제공 코드: 실습04에서 배운 fold48행의 전처리 출처를 실제로 대조합니다."""
    folds=classification_folds(dev)
    r=cross_validate(candidates()['Logistic_FE'],dev.X_train,dev.yc_train,cv=folds,
        scoring='f1',return_estimator=True,n_jobs=1,error_score='raise')
    rows=[]
    for i,((a,b),est) in enumerate(zip(folds,r['estimator']),1):
        expected=add_features(dev.X_train.iloc[a])[NUM+DERIVED].median().to_numpy()
        actual=est['pre'].named_transformers_['num']['imputer'].statistics_
        ok=bool(np.allclose(expected,actual))
        if not ok:raise AssertionError('fold 외부 통계 유입')
        rows.append({'fold':i,'fit_n':len(a),'eval_n':len(b),'chars_median':actual[0],'own_fit':ok})
    return pd.DataFrame(rows)
