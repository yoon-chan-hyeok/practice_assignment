"""Day8 실습01 03_심화: 오탐과놓침의가정비용
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

def error_costs(y,predictions,scenarios):
    """[D8-01H] 상황별 오탐·놓침 비용을 적용한 비교표를 반환합니다.
    scenarios는 상황 이름→(FP 비용, FN 비용)입니다. 반환 열은 scenario, model, FP, FN, cost입니다. 비용은 수업용 가정이며 실제 서비스의 금액을 뜻하지 않습니다.
    """
    # TODO D8-01H: 함수의 계약과 README를 보고 구현하세요.
    raise NotImplementedError("TODO D8-01H")

def main():
    y=np.array([0]*14+[1]*6);preds={'E01':np.array([0]*10+[1]*4+[0]*4+[1]*2),'All_success':np.zeros(20,dtype=int)}
    r=error_costs(y,preds,{'miss_costly':(1,5),'false_alarm_costly':(5,1)})
    out=output_dir(__file__);save_table(out/'costs.csv',r)
    policy=classification_metrics([0,0,0],[0,0,0]);policy['note']='양성0건이므로P/R/F1을0으로기록하되실제양성수를함께보고'
    save_json(out/'denominator_policy.json',policy);print(r.to_string(index=False));print_json(policy)

if __name__=="__main__":
    main()
