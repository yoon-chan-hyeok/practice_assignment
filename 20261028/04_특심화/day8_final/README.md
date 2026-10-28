# day8_final · 최종 모델링 프로젝트

실습 07에서 구현하고 실습 08에서 검증·시연합니다. 이 폴더만 별도로 복사해도 실행할 수 있습니다. 입력 경로는 현재 작업 폴더가 아니라 프로젝트 파일의 위치를 기준으로 찾습니다.

## 구현 순서
| 구분 | TODO | 수정 위치 | 재사용할 내용 |
|---|---|---|---|
| 기본필수 | D8-P01 | `feature_ops.py` / `add_features` | 실습 04의 행별 파생 변수 |
| 기본필수 | D8-P02 | `evaluate.py` / `classification_metrics` | 실습 01~02의 지표·AUC |
| 기본필수 | D8-P03 | `evaluate.py` / `choose_candidate` | 실습 06의 선택 규칙 |
| 기본필수 | D8-P04 | `evaluate.py` / `refit_development` | 개발 80건에 새 모델 재학습 |
| 실습 08 기본 | D8-P07 | `verify_submission.py` / `validate_result` | 저장 예측으로 수치 재검증 |
| 응용 | D8-P05·P06 | `persistence.py` | 모델 저장·새 프로세스 복원 |
| 심화 | D8-P08·P09 | `test_cases.py` | 필수 열 누락·동결 변경 감지 |

입출력·기존 전처리·모델 정의·CV 반복·군집 분석·동결 파일 처리는 제공됩니다. 기본필수에서는 앞 실습의 함수를 연결하여 완성합니다. 기본필수만으로 공통 100점 평가 기준을 충족할 수 있습니다.

## 환경
상위 역할 폴더의 가상환경을 사용합니다. 이 폴더를 단독으로 복사했다면 `python -m venv .venv`를 만든 뒤 **그 가상환경의 실행기**로 `python -m pip install -r requirements-lock.txt`를 수행합니다. 실행 전 `python -c "import sys; print(sys.executable)"`로 실행기를 확인합니다.

## 실행과 단계의 의미
```text
python main.py --stage develop
python main.py --stage freeze
python main.py --stage evaluate
python verify_submission.py
python main.py --stage reproduce
```

**develop**은 실험 계획을 먼저 저장한 뒤 train 60건의 동일한 5-fold로 7개 후보를 비교합니다. valid 20건은 개발 중 진단용이며 선택 함수에는 그 점수를 사용하지 않습니다. 회귀 CV, 파생 특성 비교, 군집, fold별 전처리 통계도 기록합니다.

**freeze**는 반올림 전 평균 CV F1이 가장 큰 후보를 선택합니다. 완전 동점이면 사전에 정한 후보 순서를 따릅니다. 모델·전처리·특성 규칙·임계값·입력 ID·코드·환경·데이터 해시를 저장합니다.

**evaluate**는 선택한 모델의 새 clone을 train+valid 80건에 학습한 뒤 test 20건의 입력과 정답을 가져옵니다. 실패1의 확률이 **0.5보다 클 때만** 실패로 판정하며, 정확히 0.5이면0입니다.

**verify_submission.py**는 저장한 정답·확률·예측·지표·ID를 원본과 동결 기록에 대조합니다. 보고서의 해석이나 설명 능력을 자동 채점하지 않습니다.

**reproduce**는 같은 코드·데이터·설정으로 동결 버전을 재생성하여 이전 결과와 비교합니다. 최종 지표를 덮어쓰거나 후보를 다시 선택하지 않습니다. 한 번에 실행하는 `python main.py`도 기존 평가 기록이 있으면 이 재현 단계로 이동합니다.

동결 뒤 모델 함수나 설정을 수정하면 변경 오류가 발생하는 것이 정상입니다. lock만 지워 같은 test에서 다시 선택하지 마세요. 구현 오류를 발견했다면 강사에게 알리고 교육용 재현을 수정한 사실을 기록합니다. 새 버전의 일반화 성능을 주장하려면 별도로 보관한 미사용 평가 자료가 필요합니다.

## 주요 결과
| 파일 | 기록 내용 |
|---|---|
| `outputs/cv_comparison.csv`, `cv_scores.csv` | 7개 후보의 CV 및 valid 진단 |
| `outputs/feature_comparison.csv` | 원본과 파생 변수 2개를 추가한 모델의 비교 |
| `outputs/regression_cv.csv` | RMSE(ms). 최종 회귀 test는 필수가 아님 |
| `outputs/cluster_profile.csv`, `cluster_scores.csv` | 정답 없이 학습한 군집의 개수·중심·분리도 |
| `outputs/evaluation_lock.json` | 동결한 설정·ID·해시 |
| `outputs/test_metrics.json`, `test_predictions.csv` | 확정 버전의 최종 지표와 행별 예측 |
| `reports/final_report.md` | 선택 근거·오류 사례·군집 해석·한계·개인 설명 |

`expected_outputs/`는 대조용 예시입니다. 코드 해시가 들어 있는 lock·receipt·metadata는 자신의 실행으로 만들어야 하며 예시를 복사해서 사용하면 안 됩니다.

## 응용: 저장과 새 프로세스 복원
```text
python main.py --save-model
python restore.py --trust-local
```

복원 시 Pipeline뿐 아니라 `feature_ops.py`와 관련 모듈, 같은 라이브러리 환경도 필요합니다. 대조에 사용하는 기존 valid 20건은 이미 재학습에 포함되었으므로 **재현 확인용이지 독립 성능 평가용이 아닙니다.**

joblib/pickle은 로드 과정에서 코드를 실행할 수 있습니다. 자신이 생성한 파일만 사용합니다. 해시 일치는 우발적 변경을 감지할 뿐, 외부 파일의 안전성을 보증하는 서명이 아닙니다.

## 심화와 제출
```text
python test_cases.py
```

새 범주·결측·열 누락·음수 입력·한 클래스 AUC·fold 통계·동결 변경을 검사합니다. 설정 변경 시험은 임시 복사본에서만 수행합니다.

코드, 결과 파일, 최종 보고서, 환경 기록, Git 이력, 실습 03의 회귀 지표 해석을 제출합니다. 최종 점수 자체가 높다는 이유로 가산점을 주지는 않습니다. 선택 과정과 재현성, 지표·군집의 해석 근거를 평가합니다.
