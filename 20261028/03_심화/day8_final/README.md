# day8_final · 실습06~08 통합 프로젝트

**먼저 plan.py, 다음 main.py, 마지막 restore.py입니다.** 기본·응용보다 폴더를 체계화하지만 사용자 정의 함수는 제공된 3개(`add_features`, `build`, `summarize`)를 중심으로 사용합니다. 전처리 구조를 처음부터 새로 설계하지 않습니다.

```text
day8_final/
├─ README.md
├─ plan.py              # 실습06: train CV·후보 선택·설정 기록
├─ main.py              # 실습07: 개발80 재학습·test20 평가·저장
├─ restore.py           # 실습08: 새 프로세스에서 복원·예측 대조
├─ features.py          # 제공: 행별 파생 특성
├─ preprocessing.py     # 제공: 전처리·미리 고정한 후보7개
├─ evaluate.py          # 실습07: 지표 계산 함수
├─ requirements.txt
├─ data/                # 원본100건·고정 분할(행 순서 포함)
├─ expected/            # 정답 실행으로 만든 수치·표(모델 파일 없음)
├─ outputs/             # 본인이 실행해 생성
└─ reports/
   └─ final_report.md   # 본인의 선택 근거와 한계
```

이 README와 같은 폴더를 현재 작업 폴더로 하여 실행합니다.

```bash
python -m pip install -r requirements.txt
python plan.py
python main.py
python restore.py
```

## 파일별 책임과 평가 범위

`features.py`: log_input_chars=log1p(input_chars), chars_per_slot=input_chars/(1+allowed_tools)를 같은 행에서 만듭니다. 누락 수치는 NaN으로 유지하고 뒤의 학습형 전처리가 대체합니다.

`preprocessing.py`: 전날의 Dummy·Logistic·KNN3·Tree·Forest·XGB와 Logistic_FE를 고정 순서로 제공합니다. CV를 위해 새 Pipeline을 복제하며, 학습 통계를 미리 전체 자료에서 구하지 않습니다.

`plan.py`: train60 내부5-fold의 평균F1 최대, 정확한 동점은 후보 순서로 선택합니다. valid20의 F1은 별도 진단용입니다. test20의 ID만 기록하고 입력·정답을 모델에 주지 않습니다.

`main.py`: 선택한 설정으로 **새** Pipeline을 만들고 train+valid80으로 fit합니다. 그 다음 test20을 예측합니다. 실패 확률이0.5보다 클 때만 실패1입니다. 군집은 train60 수치2열에서 별도로 계산합니다. 최종 회귀 test는 필수 과제가 아니며 회귀 학습 증거는 실습03입니다.

`restore.py`: 직접 만든 pipeline.joblib만 읽어 같은 ID 순서의 확률·판정을 대조합니다. fit과 새로운 후보 선택이 없습니다. 신뢰할 수 없는 pickle/joblib 파일은 읽지 않습니다. 다른 라이브러리 버전에서의 모델 호환성은 보장하지 않습니다. features.py도 모델과 함께 보존하세요.

## 설정 확정의 의미

본 자료의 JSON은 실험 기록입니다. 파일을 악의적 변경에서 보호하거나 test 접근을 완전히 차단하는 장치가 아닙니다. 단순한 사고 방지를 위해 plan.py는 outputs/test_metrics.json이 존재하면 기존 계획을 보존하고 종료합니다. 파일 삭제로 우회하지 마세요. 코드·데이터·임계값을 바꾸지 않은 재현과, test를 보고 변경하는 재선택을 구분합니다.

**실습07의 evaluate.py부터 확인:** `H07m`에서 F1과 AUC를 구현한 다음 main.py의 `H07a`·`H07b`를 완성하세요. main.py가 실행되더라도 지표가 임시0이면 미완성입니다.

## 실습 06 · 프로젝트 평가 계획

**목표:** 전날 후보와 파생 후보의 순서·지표를 고정하고 test 전에 선택합니다.

**열 파일:** `plan.py`

이 파일부터 시작합니다. test_metrics.json이 이미 있으면 새 선택을 하지 않고 기존 계획을 보존합니다.

### 직접 완성할 부분

- **H06**: 각 후보 Pipeline을 동일 train 5-fold로 비교하세요. 미리 전체 train을 변환하지 않습니다.

**힌트:** cross_val_score에 model 전체와 원본 X_train을 전달합니다.

### 실행

현재 README가 있는 폴더에서 다음 명령을 실행합니다. 파일 경로를 지정해 다른 작업 폴더에서 실행해도 입력을 찾도록 작성했습니다.

```bash
python plan.py
```

### 정답 구현 후의 예상 출력

소수점 마지막 자리는 환경에 따라 달라질 수 있습니다. 직접 계산하는 코드가 있어야 완료이며, 아래 숫자를 그대로 출력하는 것은 완료가 아닙니다.

```text
      model  CV_F1  CV_std  valid_F1
      Dummy 0.0000  0.0000    0.0000
   Logistic 0.5219  0.2092    0.3333
       KNN3 0.3356  0.1764    0.5455
       Tree 0.5424  0.1236    0.3333
     Forest 0.2800  0.2544    0.2222
        XGB 0.5000  0.1229    0.1818
Logistic_FE 0.5514  0.1897    0.1818
선택: Logistic_FE / 계획 저장 완료 / test20 미평가
```

**완료 기준:** TODO를 실제 계산으로 완성하고, 실행 결과를 위 기준과 대조한 뒤 아래 질문을 자신의 말로 설명합니다.

1. valid와 CV의 순위가 다르면 어떤 점수로 고르기로 했나요?

**내 설명:**

> 여기에 한두 문장으로 작성하세요.

## 실습 07 · 프로젝트 최종 실행

**목표:** 설정 선택과 평가를 파일별로 분리하고 최종 Pipeline을 저장합니다.

**열 파일:** `main.py`

먼저 plan.py로 선택을 완료하세요. evaluate.py의 TODO H07m도 main.py 실행 전에 완성합니다.

### 직접 완성할 부분

- **H07a**: 확정 모델을 개발80의 입력과 정답으로 학습하세요.
- **H07b**: 실패1의 확률을 구하세요. Feature Engineering도 저장될 Pipeline 안에서 적용됩니다.

**힌트:** 학습은 develop, 추론은 test, 요약은 evaluate.summarize가 담당합니다.

### 실행

현재 README가 있는 폴더에서 다음 명령을 실행합니다. 파일 경로를 지정해 다른 작업 폴더에서 실행해도 입력을 찾도록 작성했습니다.

```bash
python main.py
```

### 정답 구현 후의 예상 출력

소수점 마지막 자리는 환경에 따라 달라질 수 있습니다. 직접 계산하는 코드가 있어야 완료이며, 아래 숫자를 그대로 출력하는 것은 완료가 아닙니다.

```text
확정 모델: Logistic_FE / 개발80·최종20
 n  Accuracy  Precision  Recall     F1  ROC_AUC  TN  FP  FN  TP  actual_failed
20      0.75        0.6     0.5 0.5455   0.7857  12   2   3   3              6
K=3 군집
 cluster  input_chars  allowed_tools  n
       0     1542.250          4.125 24
       1     1430.474          1.368 19
       2      444.588          2.706 17
군집 silhouette: 0.453
저장: outputs/test_predictions.csv, test_metrics.json, pipeline.joblib 등
최종 성능을 본 뒤 다시 탐색하지 않습니다. 다음은 restore.py로 재현 확인입니다.
```

**완료 기준:** TODO를 실제 계산으로 완성하고, 실행 결과를 위 기준과 대조한 뒤 아래 질문을 자신의 말로 설명합니다.

1. 개발80 재학습 뒤 숫자 대체 통계가 train60 때와 달라져도 되나요?

**내 설명:**

> 여기에 한두 문장으로 작성하세요.

## 실습 08 · 저장 모델 복원

**목표:** 직접 생성한 모델 파일을 새 프로세스에서 열고 확률·예측을 대조합니다.

**열 파일:** `restore.py`

main.py가 만든 본인의 outputs/pipeline.joblib과 test_predictions.csv가 필요합니다.

### 직접 완성할 부분

- **H08**: 복원 모델로 같은 ID 순서의 실패 확률을 구하세요. fit은 호출하지 않습니다.

**힌트:** predict_proba만 호출합니다. 입력은 expected의 ID 순서대로 맞춰 두었습니다.

### 실행

현재 README가 있는 폴더에서 다음 명령을 실행합니다. 파일 경로를 지정해 다른 작업 폴더에서 실행해도 입력을 찾도록 작성했습니다.

```bash
python restore.py
```

### 정답 구현 후의 예상 출력

소수점 마지막 자리는 환경에 따라 달라질 수 있습니다. 직접 계산하는 코드가 있어야 완료이며, 아래 숫자를 그대로 출력하는 것은 완료가 아닙니다.

```text
ID 순서 동일: True
확률 동일: True
예측 동일: True
복원은 고정 버전의 재현입니다. 점수를 보고 임계값을 다시 고르지 않습니다.
```

**완료 기준:** TODO를 실제 계산으로 완성하고, 실행 결과를 위 기준과 대조한 뒤 아래 질문을 자신의 말로 설명합니다.

1. features.py를 삭제하면 저장 모델 재사용에 어떤 문제가 생길 수 있나요?

**내 설명:**

> 여기에 한두 문장으로 작성하세요.

## 결과 파일과 최종 제출

| 생성 파일 | 내용 |
|---|---|
| cv_comparison.csv · cv_scores.csv | 후보별 CV 평균/편차·valid 진단, fold별 F1 |
| feature_comparison.csv | Logistic 기본/파생의 같은 조건 비교 |
| selection.json | 후보·선택 규칙·설정·임계값·분할 ID |
| test_metrics.json · test_predictions.csv · error_cases.csv | 최종 지표·ID별 확률/예측·오류 사례 |
| cluster_profile.csv | train만 사용한 K=3 개수·원단위 중심 |
| pipeline.joblib · environment.json | 자신이 학습한 모델·실행 환경 |

`expected/`는 비교용 파일입니다. outputs로 복사하지 않습니다. 원본·계획·코드를 바꾸지 않고 main.py를 재실행하여 예측이 같은지 확인하세요. 새 터미널에서 restore.py를 실행하면 세 항목이 True여야 합니다.

**제출:** 이 프로젝트 폴더의 코드·입력·결과·requirements·보고서와 실습03 회귀CV 기록을 함께 제출합니다. `.venv`, `__pycache__`, 비밀키는 포함하지 않습니다. Git을 사용하면 자신의 변경을 1회 이상 커밋하고 README/보고서에 커밋 ID를 남깁니다. 모델 파일을 Git에 강제로 올리지는 않습니다.

```bash
git init
git add *.py README.md requirements.txt data reports
git commit -m "Complete Day8 final modeling practice"
git log -1 --oneline
```

Git 사용자 정보는 기관/개인 정책에 맞게 설정합니다. 기본필수 수강생에게 이 프로젝트의 모듈·테스트 요구를 추가하지 않습니다.
