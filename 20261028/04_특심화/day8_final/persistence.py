"""응용: 자신이 생성한 모델만 저장/복원합니다. 직렬화 파일의 출처를 확인하세요."""
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from protocol import write_json,sha256,digest,versions,CRITICAL_FILES
from preprocessing import failure_scores

def save_local_model(model,out,protocol,X_reproduction):
    """[D8-P05] fitted Pipeline을 out/final_pipeline.joblib에 저장합니다. 다시 fit하지 않습니다."""
    out=Path(out);path=out/'final_pipeline.joblib'
    # TODO D8-P05: 함수의 계약과 README를 보고 구현하세요.
    raise NotImplementedError("TODO D8-P05")
    if not path.is_file():raise AssertionError('모델 파일이 생성되지 않았습니다.')
    X_reproduction.to_csv(out/'restore_input.csv',index=True,encoding='utf-8-sig')
    score=failure_scores(model,X_reproduction)
    pd.DataFrame({'request_id':X_reproduction.index,'probability_failed':score,
        'predicted':(score>protocol['threshold']).astype(int)}).to_csv(out/'restore_expected.csv',index=False)
    root=Path(__file__).resolve().parent
    write_json(out/'model_metadata.json',{'model_sha256':sha256(path),'lock_sha256':digest(protocol),
        'versions':versions(),'code_hashes':{n:sha256(root/n) for n in CRITICAL_FILES},
        'input_sha256':sha256(out/'restore_input.csv'),'expected_sha256':sha256(out/'restore_expected.csv'),
        'notice':'기존 valid20은 재학습 이후 재현 확인용이며 독립 성능평가가 아닙니다.'})
    print('모델 저장: 자신의 final_pipeline.joblib + 코드·환경·해시·복원 대조 입력')

def load_trusted(path):
    """[D8-P06] 호출 전 출처·해시·환경을 확인한 자신의 파일을 joblib.load하여 반환합니다.
    joblib/pickle은 로드하는 도중 코드를 실행할 수 있습니다. 외부 파일을 임의로 읽지 않습니다.
    """
    # TODO D8-P06: 함수의 계약과 README를 보고 구현하세요.
    raise NotImplementedError("TODO D8-P06")
