# 2026년 10월 28일(수) · Day8 실습자료 · 수강생용

머신러닝 모델링 및 성능평가 4/4. **실습 01~08 × 기본필수·응용·심화 = 24개 활동**입니다. 실습 07~08은 동일한 `day8_final/` 프로젝트를 이어서 사용합니다.

## 수업 운영
| 실습 | 내용 | 활동 시간 |
|---|---|---:|
| 01 | 혼동행렬·지표·오류 비용 | 20분 |
| 02 | ROC·AUC·임계값 | 20분 |
| 03 | RMSE·다중 지표 CV·OOF | 25분 |
| 04 | 파생 특성·동일 조건 비교·fold 통계 | 25분 |
| 05 | K-Means·중심·군집 해석 | 25분 |
| 06 | 설정 확정·80건 재학습·test 평가 | 25분 |
| 07 | 최종 프로젝트 통합 | 25분 |
| 08 | 검증·보고서·시연 | 35분 |

실습·리뷰 합계는 200분입니다. 각 시간의 기본필수가 공통 목표이며 응용·심화는 선택 확장입니다. 전공 여부로 난이도를 고정하지 않습니다. 시작 전에 예상값을 적고, 실행 후 실제값과 비교합니다.

## 환경 준비
기존 강의용 환경의 버전이 같으면 그대로 사용합니다. 다르면 별도 가상환경을 만들어 다른 프로젝트의 환경을 덮어쓰지 않습니다. 아래 명령은 이 README가 있는 역할 폴더에서 실행합니다.

Windows PowerShell:
```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe check_env.py
```

`py`가 없으면 설치된 Python 3.13의 `python -m venv .venv`를 사용합니다. VS Code의 **Python: Select Interpreter**에서 `.venv`를 선택합니다. 실행기를 위처럼 직접 지정하면 활성화 스크립트를 위한 실행 정책 변경은 필요하지 않습니다.

macOS/Linux:
```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements-lock.txt
.venv/bin/python check_env.py
```

이후 안내의 `python`은 선택한 가상환경 실행기를 뜻합니다. 확인한 환경은 Python 3.13.5·NumPy 2.3.5·pandas 2.2.3·scikit-learn 1.8.0·XGBoost 3.1.3입니다. CPU만 사용하며 데이터 다운로드나 외부 AI API 호출은 없습니다. **Linux에서 실행 검사했고, Windows/macOS에서 직접 실행한 검증은 하지 않았습니다.**

## 첫 실습
```text
python "ex01_metrics/01_기본필수/main.py"
python tools/check_practice.py --exercise 1 --level basic
```

수강생용 코드에서 `NotImplementedError`가 발생하면 표시된 TODO 함수를 구현해야 합니다. 이는 문법 오류가 아니라 의도적으로 비워 둔 부분입니다. 함수의 입력·반환값, 힌트, 완료 기준은 각 폴더의 README에 있습니다.

## 폴더 구성
| 경로 | 역할 |
|---|---|
| `data/` | 전날과 같은 합성 요청 100건, 분할표·행 순서, 경계·실패 입력 |
| `ex01_...`~`ex06_...` | 개별 함수 실습. 실행 결과는 각 단계의 `outputs/`에 생성 |
| `ex07_...`, `ex08_...` | 공통 프로젝트의 난이도별 안내와 실행 연결 |
| `day8_final/` | 별도로 복사해도 실행되는 최종 VS Code 프로젝트 |
| `tools/`, `tests/` | 수치·입력 계약 검사. 보고서의 판단을 대신 채점하지 않음 |
| `worksheets/` | 평가·보고서·코드리뷰·테스트·만족도 양식 |

`expected_output.txt`와 `expected_outputs/`는 정답 코드를 실제 실행해 만든 **대조용 결과**입니다. 이 파일을 읽어 계산을 대신하거나 자신의 `outputs/`로 복사하지 않습니다. 특히 동결 기록의 해시는 작성한 코드·환경에 따라 달라지므로 자신의 프로그램으로 생성해야 합니다.

## 최종 프로젝트 실행
```text
python day8_final/main.py --stage develop
python day8_final/main.py --stage freeze
python day8_final/main.py --stage evaluate
python day8_final/verify_submission.py
python day8_final/main.py --stage reproduce
```

처음 세 단계는 `python day8_final/main.py`로 연결할 수도 있습니다. 이미 최종 평가 기록이 있으면 모델을 다시 선택하지 않고 **동결된 버전의 재현만 확인**합니다.

후보·특성 규칙·주 지표·임계값을 확정한 뒤 새 Pipeline을 개발 데이터 80건에 재학습합니다. test 20건은 그 이후에 평가합니다. 기존 valid 20건은 재학습에 포함되므로 더 이상 독립 평가 자료가 아닙니다.

PPT에 최종 test 결과가 이미 공개되어 있으므로 이 과정은 **교육용 재현**입니다. 새로운 블라인드 연구 결과나 실제 서비스 성능으로 주장하지 않습니다. 동결 파일과 해시는 우발적인 변경을 감지하는 장치이며 데이터에 대한 접근 권한을 통제하는 보안 장치는 아닙니다.

## 검사 명령
```text
python tools/check_practice.py --all
python -m unittest discover -s tests -v
python day8_final/test_cases.py
```

`--all`은 실습 01~06의 18개 단계를 실행합니다. 아직 구현하지 않은 응용·심화는 실패하므로 완성한 단계만 선택해 검사해도 됩니다. 프로젝트 심화 검사는 기본 프로젝트를 실행한 후 수행합니다.

## 제출과 협업
코드·실험표·보고서·환경·Git 이력을 함께 제출합니다. `.venv`, 외부 출처의 신뢰할 수 없는 모델 파일, API 키·비밀번호는 넣지 않습니다. 모델 저장·복원은 자신이 실행하여 만든 파일로 수행합니다. 학습된 joblib 파일은 이 패키지에 미리 넣지 않았습니다.

익명 만족도 응답은 성적과 분리하여 수집합니다. 개인별 지원 요청이 필요하면 만족도 양식과 별도의 창구를 사용합니다.

## 배포 원본 무결성 확인
수정하기 전에 `python tools/verify_files.py`로 파일 누락·변경을 확인할 수 있습니다. 학습자가 TODO를 완성한 뒤에는 소스 해시가 달라지는 것이 정상입니다. 이 검사는 성적 평가가 아닙니다.

`unittest discover`에도 응용·심화 함수 검사가 포함되어 있습니다. 기본필수만 수행하는 수강생은 완성한 단계의 개별 검사와 `day8_final/verify_submission.py`를 우선 실행합니다. 미수행 선택 과제의 TODO 때문에 전체 검사가 실패한 것은 공통 평가의 감점 사유가 아닙니다.
