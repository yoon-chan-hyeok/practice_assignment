"""제공 설정: PPT의 후보·seed·CPU 설정. 여기에는 학습된 객체/결과가 없습니다."""
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.model_selection import StratifiedKFold, KFold

def new_classifier(name: str):
    if name == 'Dummy': return DummyClassifier(strategy='most_frequent')
    if name == 'Logistic': return LogisticRegression(C=1, max_iter=1000)
    if name == 'KNN3': return KNeighborsClassifier(n_neighbors=3)
    if name == 'Tree':
        return DecisionTreeClassifier(max_depth=3, min_samples_leaf=3, random_state=42)
    if name == 'Forest':
        return RandomForestClassifier(n_estimators=100, max_depth=4,
            min_samples_leaf=2, max_features='sqrt', random_state=42, n_jobs=1)
    if name == 'XGB':
        # XGBoost가 없어도 실습01~04는 실행 가능합니다. 05부터는 반드시 설치합니다.
        from xgboost import XGBClassifier
        return XGBClassifier(n_estimators=80, max_depth=2, learning_rate=0.05,
            min_child_weight=1, subsample=0.8, colsample_bytree=1.0, reg_lambda=1.0,
            objective='binary:logistic', eval_metric='logloss', tree_method='hist',
            device='cpu', random_state=42, n_jobs=1)
    raise ValueError(f'알 수 없는 분류 모델: {name}')

def new_regressor(name: str):
    if name == 'Dummy': return DummyRegressor(strategy='mean')
    if name == 'Linear': return LinearRegression()
    if name == 'KNN15': return KNeighborsRegressor(n_neighbors=15)
    if name == 'Tree':
        return DecisionTreeRegressor(max_depth=3, min_samples_leaf=3, random_state=42)
    if name == 'Forest':
        return RandomForestRegressor(n_estimators=100, max_depth=4,
            min_samples_leaf=2, max_features=1.0, random_state=42, n_jobs=1)
    if name == 'XGB':
        from xgboost import XGBRegressor
        return XGBRegressor(n_estimators=80, max_depth=2, learning_rate=0.05,
            min_child_weight=1, subsample=0.8, colsample_bytree=1.0, reg_lambda=1.0,
            objective='reg:squarederror', eval_metric='rmse', tree_method='hist',
            device='cpu', random_state=42, n_jobs=1)
    raise ValueError(f'알 수 없는 회귀 모델: {name}')

def make_folds(X, y, task='classification'):
    """train 내부 위치 인덱스. 위치를 request_id와 혼동하지 않습니다."""
    if not X.index.equals(y.index):
        raise ValueError('X/y 인덱스와 순서가 일치해야 합니다.')
    if task == 'classification':
        if set(y.dropna().unique()) != {0,1} or y.isna().any():
            raise ValueError('분류 CV는 결측 없는 두 클래스 0/1이 모두 필요합니다.')
        if y.value_counts().min() < 5:
            raise ValueError('5-fold에는 각 클래스가 최소 5건 필요합니다.')
        splitter = StratifiedKFold(5, shuffle=True, random_state=42)
        return list(splitter.split(X, y))
    if task == 'regression':
        return list(KFold(5, shuffle=True, random_state=42).split(X))
    raise ValueError(task)

def fold_table(X, folds, task='classification'):
    """누가 어디에 속했는지 남기는 감사용 표. 점수는 이 함수에서 계산하지 않습니다."""
    rows=[]
    for i,(a,b) in enumerate(folds,1):
        if set(a)&set(b): raise ValueError('fold 학습/평가 중복')
        for role,positions in [('fit',a),('evaluate',b)]:
            for p in positions:
                rows.append({'task':task,'fold':i,'role':role,
                             'position_in_train':int(p),'request_id':X.index[p]})
    return pd.DataFrame(rows)
