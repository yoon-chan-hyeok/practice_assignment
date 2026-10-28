"""Day8 실습03 03_심화: fold평균과OOF의차이
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
from sklearn.model_selection import cross_validate,cross_val_predict
from sklearn.metrics import f1_score

def compare_oof(dev):
    """[D8-03H] fold 평균 F1과 합친 OOF F1을 따로 보고합니다.
    반환값은 (fold 표, ID별 OOF 표, 요약 dict)입니다. 요약 키는 fold_mean_F1, pooled_OOF_F1입니다. F1은 비선형 비율이므로 두 계산 결과가 같아야 하는 것은 아닙니다.
    """
    # TODO D8-03H: 함수의 계약과 README를 보고 구현하세요.
    raise NotImplementedError("TODO D8-03H")

def main():
    a,b,c=compare_oof(load_data());out=output_dir(__file__);save_table(out/'fold_scores.csv',a);save_table(out/'oof_predictions.csv',b)
    save_json(out/'comparison.json',c);print(a.round(3).to_string(index=False));print_json(c)

if __name__=="__main__":
    main()
