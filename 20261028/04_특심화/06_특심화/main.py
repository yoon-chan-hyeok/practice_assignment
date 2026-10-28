"""Day8 실습06 03_심화: 동결변경감지
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
import tempfile,shutil,json

def reject_changed_lock(out):
    """[D8-06H] 동결 뒤 임계값이 바뀌면 검증이 거부하는지 확인합니다.
    실제 outputs를 건드리지 않고 임시 복사본에서 threshold를0.3으로 바꿉니다. 검증 함수가 ValueError를 내면 True, 거부하지 않으면 AssertionError입니다.
    """
    # TODO D8-06H: 함수의 계약과 README를 보고 구현하세요.
    raise NotImplementedError("TODO D8-06H")

def main():
    from workflow_support import run_mini
    out=output_dir(__file__);run_mini(out);ok=reject_changed_lock(out)
    save_json(out/'tamper_check.json',{'changed_threshold_rejected':ok,'original_preserved':True})
    print('동결뒤임계값변경거부:',ok)

if __name__=="__main__":
    main()
