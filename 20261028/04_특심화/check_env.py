"""실제 Python 실행기·패키지·CPU 모델 동작을 확인합니다. 설치나 환경 변경은 하지 않습니다."""
from pathlib import Path
import sys,platform,importlib,importlib.metadata,json
EXPECTED={'numpy':'2.3.5','pandas':'2.2.3','scipy':'1.17.0','scikit-learn':'1.8.0','xgboost':'3.1.3','joblib':'1.5.3','matplotlib':'3.10.8','threadpoolctl':'3.6.0'}
MODULES={'scikit-learn':'sklearn'}
def main():
    print('Python:',platform.python_version());print('실행기:',sys.executable);print('운영체제:',platform.system())
    errors=[];mismatches=[]
    for name,expected in EXPECTED.items():
        try:
            importlib.import_module(MODULES.get(name,name));actual=importlib.metadata.version(name)
            print(f'{name}: {actual} (검증버전 {expected})')
            if actual!=expected:mismatches.append(name)
        except Exception as exc:errors.append(f'{name}: {type(exc).__name__}: {exc}')
    if errors:
        print('\n'.join(errors));print('선택한 가상환경에서 requirements-lock.txt 설치 및 원래 오류를 확인하세요.');return 1
    import numpy as np
    from xgboost import XGBClassifier
    model=XGBClassifier(n_estimators=2,max_depth=1,tree_method='hist',device='cpu',n_jobs=1,random_state=42)
    x=np.array([[0.],[1.],[2.],[3.],[4.],[5.]])
    model.fit(x,np.array([0,0,0,1,1,1]));model.predict(x)
    print('XGBoost CPU 실행: 통과 / GPU·외부 API 불필요')
    if mismatches or platform.python_version()!='3.13.5':print('버전 차이 있음: 예상값은 검증환경 기준입니다. 버전 기록과 추가 확인이 필요합니다.')
    return 0
if __name__=='__main__':sys.exit(main())
