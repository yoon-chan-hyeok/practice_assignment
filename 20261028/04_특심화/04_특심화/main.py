"""Day8 실습04 03_심화: fold내부통계감사
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
from sklearn.model_selection import cross_validate

def audit_fold_medians(dev):
    """[D8-04H] 각 fold의 전처리 통계가 그 학습48행에서 왔는지 검사합니다.
    cross_validate의 return_estimator로 각 fitted Pipeline을 얻습니다. 해당48행의 파생 표에서 직접 계산한 중앙값과 imputer.statistics_를 대조합니다. fold/fit_n/eval_n/chars_median/own_fit 열을 반환합니다.
    """
    # TODO D8-04H: 함수의 계약과 README를 보고 구현하세요.
    raise NotImplementedError("TODO D8-04H")

def main():
    r=audit_fold_medians(load_data());save_table(output_dir(__file__)/'fold_statistics.csv',r);print(r.to_string(index=False))
    if not r.own_fit.all():raise AssertionError('fold외부통계유입')

if __name__=="__main__":
    main()
