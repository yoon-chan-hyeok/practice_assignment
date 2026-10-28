"""응용: 새 프로세스에서 자신의 모델만 복원합니다. --trust-local이 필요합니다."""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
from protocol import read_json,write_json,sha256,verify_lock,digest,versions
from data_io import load_data,read_table,FEATURES
from preprocessing import failure_scores
from persistence import load_trusted
ROOT=Path(__file__).resolve().parent

def restore(out,trust_local=False):
    out=Path(out)
    if not trust_local:raise ValueError('직접 생성한 파일의 출처를 확인한 뒤 --trust-local을 명시하세요.')
    p=verify_lock(out,load_data(ROOT/'data'),ROOT);m=read_json(out/'model_metadata.json')
    if m['versions']!=versions():raise ValueError('저장 때와 패키지 버전이 다릅니다.')
    if m['lock_sha256']!=digest(p) or m['model_sha256']!=sha256(out/'final_pipeline.joblib'):raise ValueError('설정 또는 모델 파일 변경')
    if any(sha256(ROOT/n)!=h for n,h in m['code_hashes'].items()):raise ValueError('변환 코드 변경')
    if sha256(out/'restore_input.csv')!=m['input_sha256'] or sha256(out/'restore_expected.csv')!=m['expected_sha256']:raise ValueError('복원 대조 파일 변경')
    # 해시는 실수/변경을 감지할 뿐, 악성 파일의 안전성을 증명하는 서명은 아닙니다.
    model=load_trusted(out/'final_pipeline.joblib');x=read_table(out/'restore_input.csv').set_index('request_id')[FEATURES]
    old=pd.read_csv(out/'restore_expected.csv');score=failure_scores(model,x);pred=(score>p['threshold']).astype(int)
    if x.index.tolist()!=old.request_id.tolist() or not np.array_equal(pred,old.predicted) or not np.allclose(score,old.probability_failed,rtol=1e-10,atol=1e-12):raise AssertionError('복원 예측 불일치')
    write_json(out/'restore_check.json',{'new_process':True,'probabilities_match':True,'predictions_match':True,'n':len(x),
        'feature_function_module':model['features'].func.__module__ if 'features' in model.named_steps else None})
    print('새 프로세스 복원: 확률·예측·ID 일치 / 기존 valid20은 재현 확인용')
    return True
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ROOT/'outputs');p.add_argument('--trust-local',action='store_true');a=p.parse_args();restore(a.output.resolve(),a.trust_local)
