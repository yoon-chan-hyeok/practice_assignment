"""Day8 실습05 03_심화: 번호대신소속구조비교
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
from sklearn.metrics import adjusted_rand_score

def compare_cluster_labels(a,b):
    """[D8-05H] 군집 번호가 아니라 소속 구조가 같은지 비교합니다.
    같은 길이의 두1차원 라벨을 받아 same_number_fraction, ARI, same_partition을 반환합니다. 쌍별로 같은 군집인지 확인하면 번호가 바뀐 동일한 묶음을 구분할 수 있습니다.
    """
    # TODO D8-05H: 함수의 계약과 README를 보고 구현하세요.
    raise NotImplementedError("TODO D8-05H")

def main():
    a=np.array([0,0,0,1,1,1]);r=compare_cluster_labels(a,1-a);save_json(output_dir(__file__)/'label_permutation.json',r);print_json(r)
    print('확장설계: KMeans.transform을특성으로쓸때수치전처리와군집학습도CV안에넣습니다.')

if __name__=="__main__":
    main()
