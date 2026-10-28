"""실습08: 수치·ID·파일의 관계를 확인합니다. 보고서와 개인 설명의 평가를 대신하지 않습니다."""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
from data_io import load_data,read_table,sha256,save_json
from protocol import verify_lock,read_json
from evaluate import classification_metrics
ROOT=Path(__file__).resolve().parent

def validate_result(frame,metrics,expected_ids,threshold):
    """[D8-P07] 저장 예측으로 지표를 재계산하고 오류 문자열 목록을 반환합니다.
    ID/순서·예측=확률>threshold·Accuracy/P/R/F1/AUC·혼동행렬·n/positive_n을 비교합니다.
    한 클래스 AUC는None과일치해야합니다. 계산 오차는np.isclose로비교합니다.
    """
    # TODO D8-P07: 함수의 계약과 README를 보고 구현하세요.
    raise NotImplementedError("TODO D8-P07")

def verify(out):
    out=Path(out);dev=load_data(ROOT/'data');p=verify_lock(out,dev,ROOT);receipt=read_json(out/'evaluation_receipt.json')
    if sha256(out/'test_predictions.csv')!=receipt['predictions_sha256'] or sha256(out/'test_metrics.json')!=receipt['metrics_sha256']:raise ValueError('최종 평가 후 결과 파일 변경')
    frame=pd.read_csv(out/'test_predictions.csv');metrics=read_json(out/'test_metrics.json')
    errors=validate_result(frame,metrics,p['heldout_ids'],p['threshold'])
    raw=read_table(ROOT/'data/requests.csv').set_index('request_id')
    if not np.array_equal(frame.actual.to_numpy(),raw.loc[p['heldout_ids'],'failed'].to_numpy()):errors.append('저장 정답과 원본 불일치')
    if not pd.read_csv(out/'fold_statistics.csv').own_fit.all():errors.append('fold 학습 통계 오류')
    if pd.read_csv(out/'cluster_profile.csv').n.sum()!=60:errors.append('군집 표본 수 오류')
    if errors:raise AssertionError('\n'.join(errors))
    save_json(out/'submission_checks.json',{'numeric_and_file_checks':'passed','human_report_and_explanation':'not_automatically_graded'})
    print('제출 검증: ID·정답·임계값·지표·fold 통계·군집·동결 해시 통과')
    return True
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=ROOT/'outputs');args=parser.parse_args();verify(args.output.resolve())
