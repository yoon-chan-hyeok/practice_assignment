"""Day8 실습02 03_심화: AUC계산불가와OOF탐색
입력·반환값·실행법·완료기준은README.md를확인합니다.
"""
from pathlib import Path
import os,sys
os.environ.setdefault('OMP_NUM_THREADS','1')
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
# [제공] 다른 작업 폴더에서 실행해도 배포 폴더를 찾도록 하는 제공 코드입니다.
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'course_support.py').is_file())
sys.path.insert(0,str(ROOT))
import numpy as np
import pandas as pd
from course_support import (load_data,output_dir,save_json,save_table,print_json,NUM,CAT,
    FEATURES,DERIVED,check_features,classification_folds,regression_folds)
from model_support import (build,build_with_features,candidates,feature_reference,
    failure_scores,classification_metrics,numeric_cluster,CANDIDATE_ORDER)
from sklearn.metrics import roc_auc_score,f1_score,recall_score
from sklearn.model_selection import cross_val_predict

def safe_auc(y,score):
    """[D8-02H1] AUC를 계산할 수 없는 입력을 명시적으로 구분합니다.
    정답에 두 클래스가 있으면 float, 한 클래스면 None을 반환합니다. 빈 입력, 길이 불일치,0/1이 아닌 정답, NaN/inf 점수는 ValueError로 거부합니다. None을0으로 바꾸어 나쁜 성능처럼 표현하지 않습니다.
    """
    # TODO D8-02H1: 함수의 계약과 README를 보고 구현하세요.
    raise NotImplementedError("TODO D8-02H1")

def oof_threshold_study(dev):
    """[D8-02H2] train60의 OOF 확률로 임계값 후보를 탐색합니다.
    고정 Logistic의 동일5-fold 예측으로0.3/0.5/0.7의 threshold, F1, Recall 표를 반환합니다. 자기 행을 학습하지 않은 모델의 점수를 사용하되, 임계값 선택에 쓴 점수는 독립 최종 성능이 아닙니다. 기본 최종평가의0.5 정책과 분리합니다.
    """
    # TODO D8-02H2: 함수의 계약과 README를 보고 구현하세요.
    raise NotImplementedError("TODO D8-02H2")

def main():
    out=output_dir(__file__);policy={'AUC':safe_auc([0,0,0],[.1,.2,.3]),'positive_n':0,'reason':'한클래스'}
    save_json(out/'single_class.json',policy);r=oof_threshold_study(load_data());save_table(out/'oof_threshold_study.csv',r)
    print_json(policy);print(r.round(3).to_string(index=False));print('OOF임계값선택용: test미사용, 최종성능추정치아님')

if __name__=="__main__":
    main()
