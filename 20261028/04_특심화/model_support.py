"""제공 코드: 전날 Pipeline 및 실습 간 재사용용 모델. 학습된 가중치는 없습니다.
feature_reference는독립실습을위한제공규칙입니다. 실습04에서는동일규칙을직접구현합니다.
"""
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,OneHotEncoder,FunctionTransformer
from sklearn.linear_model import LogisticRegression,LinearRegression
from sklearn.neighbors import KNeighborsClassifier,KNeighborsRegressor
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import (confusion_matrix,accuracy_score,precision_score,recall_score,f1_score,roc_auc_score)
from xgboost import XGBClassifier
from course_support import NUM,CAT,FEATURES,DERIVED,check_features
check_input=check_features
CANDIDATE_ORDER=['Dummy','Logistic','KNN3','Tree','Forest','XGB','Logistic_FE']


def feature_reference(X):
    """원본을 바꾸지 않는 행별 파생 변수. y·다른 행의 통계는 사용하지 않는다.
    chars_per_slot = input_chars/(1+allowed_tools). 실제 도구 사용량/시간이 아니다.
    """
    out=check_input(X)
    out['log_input_chars']=np.log1p(out['input_chars'])
    out['chars_per_slot']=out['input_chars']/(1.0+out['allowed_tools'])
    return out

def make_pre(engineered=False,scale=True):
    nums=NUM+DERIVED if engineered else NUM
    nsteps=[('imputer',SimpleImputer(strategy='median',keep_empty_features=True))]
    if scale: nsteps.append(('scaler',StandardScaler()))
    cat=Pipeline([('imputer',SimpleImputer(strategy='most_frequent',keep_empty_features=True)),
        ('encoder',OneHotEncoder(handle_unknown='ignore',sparse_output=False))])
    return ColumnTransformer([('num',Pipeline(nsteps),nums),('cat',cat,CAT)],remainder='drop')

def build(model,engineered=False,scale=True):
    steps=[]
    if engineered: steps.append(('features',FunctionTransformer(feature_reference,validate=False)))
    steps += [('pre',make_pre(engineered,scale)),('model',clone(model))]
    return Pipeline(steps)

def candidates():
    """후보는 test 확인 전에 고정. Day7의 6후보에 Logistic_FE만 추가한다."""
    return {
        'Dummy':build(DummyClassifier(strategy='most_frequent')),
        'Logistic':build(LogisticRegression(C=1,max_iter=1000)),
        'KNN3':build(KNeighborsClassifier(n_neighbors=3)),
        'Tree':build(DecisionTreeClassifier(max_depth=3,min_samples_leaf=3,random_state=42),scale=False),
        'Forest':build(RandomForestClassifier(n_estimators=100,max_depth=4,min_samples_leaf=2,
             max_features='sqrt',random_state=42,n_jobs=1),scale=False),
        'XGB':build(XGBClassifier(n_estimators=80,max_depth=2,learning_rate=0.05,
             min_child_weight=1,subsample=0.8,colsample_bytree=1.0,reg_lambda=1.0,
             objective='binary:logistic',eval_metric='logloss',tree_method='hist',
             device='cpu',random_state=42,n_jobs=1),scale=False),
        'Logistic_FE':build(LogisticRegression(C=1,max_iter=1000),engineered=True)
    }

def failure_scores(model,X):
    """classes_에서 실패1의 열을 찾는다. 확률 열의 순서를 가정하지 않는다."""
    k=np.flatnonzero(model.classes_==1)
    if len(k)!=1: raise ValueError('실패 클래스1이 학습되지 않았습니다.')
    return model.predict_proba(X)[:,int(k[0])]

def classification_metrics(y,pred,score=None):
    tn,fp,fn,tp=confusion_matrix(y,pred,labels=[0,1]).ravel()
    out={'Accuracy':float(accuracy_score(y,pred)),
         'Precision':float(precision_score(y,pred,pos_label=1,zero_division=0)),
         'Recall':float(recall_score(y,pred,pos_label=1,zero_division=0)),
         'F1':float(f1_score(y,pred,pos_label=1,zero_division=0)),
         'TN':int(tn),'FP':int(fp),'FN':int(fn),'TP':int(tp),'n':len(y),
         'positive_n':int(np.sum(np.asarray(y)==1))}
    if score is not None:
        out['ROC_AUC']=float(roc_auc_score(y,score)) if len(np.unique(y))==2 else None
    return out

def numeric_cluster(X,k=3):
    # 군집화는 y를 받지 않는다. train 수치2열만 사용하며 범주/정답은 넣지 않는다.
    pipe=Pipeline([('imputer',SimpleImputer(strategy='median',keep_empty_features=True)),
                   ('scaler',StandardScaler()),
                   ('cluster',KMeans(n_clusters=k,init='k-means++',n_init=10,random_state=42))])
    return pipe.fit(X[NUM])

def build_with_features(model,fn):
    return Pipeline([('features',FunctionTransformer(fn,validate=False)),
                     ('pre',make_pre(True)),('model',clone(model))])
