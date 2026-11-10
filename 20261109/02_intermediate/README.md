# Day16 · 02_응용 · 수강생용

이 README 하나로 실습 01~08을 진행합니다. 전체 환경 준비는 상위 `README.md`를 읽습니다.

코드는 바로 보이는 위치에 두고 원본은 `data/`, 결과는 `outputs/`로 분리합니다.

**실제 OCR:** 기본필수 02는 Tesseract+eng가 필요합니다. 다른 파일은 제공 OCR 기록으로 독립 실행됩니다. VLM은 mock, 배포는 설계입니다.

## 실습 01 · 원근·적응형 이진화 — PPT 19쪽

**목표:** 알려진 네 모서리를 사용해 문서를 펴 봅니다.

**열 파일:** `01_rectify.py`

**A01 요구사항:** 제공한 투시 변환행렬과 (width,height)로 warpPerspective를 호출하세요.

**함수·인자 설명:** warpPerspective(src, M, dsize): 필수 3개. interpolation·borderMode 등은 선택입니다.

실행 위치: 이 README가 있는 폴더. 입력·출력은 파일 위치를 기준으로 찾습니다.

```powershell
python 01_rectify.py
```

**제작 환경의 실제 실행 출력:**

```text
before: (800, 1100, 3) after: (700, 1000, 3)
알려진 모서리로 보정했습니다. 모서리 자동 검출이 아닙니다.
```

**생성 결과:** outputs/p01_*.png

**완료 기준:** TODO 구현, 파일 재읽기·수치 확인, 아래 설명을 모두 완료합니다. OCR 버전별 글자·confidence는 달라질 수 있으므로 자신의 결과와 차이를 적습니다.

**설명 질문:** 그림을 단순 resize한 결과와 원근 보정한 결과는 어떻게 다를까요?

내 설명: __________________________________________

## 실습 02 · 단어 Box·PSM — PPT 29쪽

**목표:** 기록된 실제 단어 좌표를 원본 위에 확인합니다.

**열 파일:** `02_boxes.py`

**A02 요구사항:** 각 단어 bbox를 파란 선으로 그리세요. xyxy의 마지막 좌표는 픽셀 경계입니다.

**함수·인자 설명:** rectangle(img, pt1, pt2, color, thickness=1)는 앞 네 인자 필수입니다. OCR 좌표와 이미지 크기가 같아야 합니다.

실행 위치: 이 README가 있는 폴더. 입력·출력은 파일 위치를 기준으로 찾습니다.

```powershell
python 02_boxes.py
```

**제작 환경의 실제 실행 출력:**

```text
단어: 27 backend: tesseract_recorded
PSM 3: 전체 문서 / PSM 6: 균일한 글 블록 / PSM 7: 한 줄 crop
PSM 3 whole_page -> 'INVOICE DOCO1\n\nDATE: 2026-11-01\nSUPPLIER: BLUE CAFE\nITEM QTY PRIC'
PSM 7 single_total_line -> 'TOTAL: 27000'
PSM 6 whole_page -> 'INVOICE DOCO1\nDATE: 2026-11-01\nSUPPLIER: BLUE CAFE\nITEM QTY PRICE'
PSM 7은 한 줄 crop입니다. 전체 페이지와 입력 범위가 다르므로 CER을 직접 순위화하지 않습니다.
```

**생성 결과:** outputs/p02_word_boxes.png

**완료 기준:** TODO 구현, 파일 재읽기·수치 확인, 아래 설명을 모두 완료합니다. OCR 버전별 글자·confidence는 달라질 수 있으므로 자신의 결과와 차이를 적습니다.

**설명 질문:** 단일 행 crop과 전체 페이지에 같은 PSM을 쓰면 어떤 차이가 날까요?

내 설명: __________________________________________

## 실습 03 · 근거 좌표를 가진 필드 — PPT 39쪽

**목표:** raw·value·confidence·bbox를 묶어 저장합니다.

**열 파일:** `03_evidence.py`

**A03 요구사항:** 같은 글줄이며 라벨 오른쪽에 있는 단어만 골라 selected에 넣으세요. 줄 번호 하나만 비교하면 안 됩니다.

**함수·인자 설명:** next(iterator)는 첫 항목을 선택합니다. 이 단계는 모든 라벨이 존재하는 정상 데이터로 진행합니다.

실행 위치: 이 README가 있는 폴더. 입력·출력은 파일 위치를 기준으로 찾습니다.

```powershell
python 03_evidence.py
```

**제작 환경의 실제 실행 출력:**

```text
{'issued_at': '2026-11-01', 'supplier': 'BLUE CAFE', 'total_amount': 27000}
```

**생성 결과:** outputs/p03_evidence.json

**완료 기준:** TODO 구현, 파일 재읽기·수치 확인, 아래 설명을 모두 완료합니다. OCR 버전별 글자·confidence는 달라질 수 있으므로 자신의 결과와 차이를 적습니다.

**설명 질문:** 단어 순서를 y좌표만으로 정렬하면 다단 문서에서 왜 문제가 될까요?

내 설명: __________________________________________

## 실습 04 · VLM 근거 점검 — PPT 52쪽

**목표:** 정답 여부·형식·근거를 서로 구분합니다.

**열 파일:** `04_mock_compare.py`

**A04 요구사항:** evidence가 해당 문서의 OCR 원문에 있는지 검사하세요. 다른 문서의 문장을 근거로 쓰지 않습니다.

**함수·인자 설명:** in은 부분 문자열 검사입니다. 상위 단계는 라벨과 값 일치도 추가 검사합니다.

실행 위치: 이 README가 있는 폴더. 입력·출력은 파일 위치를 기준으로 찾습니다.

```powershell
python 04_mock_compare.py
```

**제작 환경의 실제 실행 출력:**

```text
mock 필드: 15 근거 문자열 발견: 13
모의 응답의 평가 연습이며 실제 VLM 정확도가 아닙니다.
```

**생성 결과:** outputs/p04_mock_review.csv

**완료 기준:** TODO 구현, 파일 재읽기·수치 확인, 아래 설명을 모두 완료합니다. OCR 버전별 글자·confidence는 달라질 수 있으므로 자신의 결과와 차이를 적습니다.

**설명 질문:** 정답값이 맞더라도 근거가 없는 답을 어떻게 표시할까요?

내 설명: __________________________________________

## 실습 05 · 값과 근거의 분리 평가 — PPT 62쪽

**목표:** 15개 필드의 값 일치와 근거 유무를 따로 보고합니다.

**열 파일:** `05_field_metrics.py`

**A05 요구사항:** 정답 키를 오직 평가에 사용해 값 일치 여부를 계산하세요.

**함수·인자 설명:** bool 열의 sum은 True 개수, &는 항목별 논리 AND입니다.

실행 위치: 이 README가 있는 폴더. 입력·출력은 파일 위치를 기준으로 찾습니다.

```powershell
python 05_field_metrics.py
```

**제작 환경의 실제 실행 출력:**

```text
값 일치: 14 / 15
값과 문자열 근거: 13 / 15
추론 지연시간: N/A (mock)
```

**생성 결과:** outputs/p05_scores.csv

**완료 기준:** TODO 구현, 파일 재읽기·수치 확인, 아래 설명을 모두 완료합니다. OCR 버전별 글자·confidence는 달라질 수 있으므로 자신의 결과와 차이를 적습니다.

**설명 질문:** 모의 응답 파일 읽기 시간을 실제 모델 추론시간이라고 할 수 있나요?

내 설명: __________________________________________

## 실습 06 · 엔진 설계·버전 구분 — PPT 73쪽

**목표:** 동적 shape와 빌드 환경을 명시합니다.

**열 파일:** `06_engine_plan.py`

**A06 요구사항:** TensorRT 10.x 전용 명령의 ONNX·engine·동적 profile·FP16 옵션을 작성하세요. 실행하지 않습니다.

**함수·인자 설명:** 11.x는 강한 타입 모델에서 정밀도를 결정하므로 --fp16을 그대로 넣지 않습니다. 실제 support matrix를 우선합니다.

실행 위치: 이 README가 있는 폴더. 입력·출력은 파일 위치를 기준으로 찾습니다.

```powershell
python 06_engine_plan.py
```

**제작 환경의 실제 실행 출력:**

```text
설계만: trtexec --onnx=model.onnx --saveEngine=model.plan --minShapes=images:1x3x224x224 --optShapes=images:4x3x224x224 --maxShapes=images:8x3x224x224 --fp16
11.x는 --fp16 제거. ONNX 정밀도 변환을 사전에 하고 설치 버전의 help를 확인.
```

**생성 결과:** outputs/p06_engine_manifest.json

**완료 기준:** TODO 구현, 파일 재읽기·수치 확인, 아래 설명을 모두 완료합니다. OCR 버전별 글자·confidence는 달라질 수 있으므로 자신의 결과와 차이를 적습니다.

**설명 질문:** 같은 engine.plan이 Windows·Linux·다른 Jetson에서 항상 열릴까요?

내 설명: __________________________________________

## 실습 07 · Hybrid 미니 프로젝트 — PPT 83쪽

**목표:** OCR 원문과 모의 답변을 합치되 불일치를 검토로 남깁니다.

**열 파일:** `07_project.py`

**A07 요구사항:** OCR 원문에서 세 필드를 추출하세요. 정답값과 모의 VLM 답변을 가져오지 않습니다.

**A08 요구사항:** OCR 값과 답이 다르거나 evidence가 없으면 review=True로 기록하세요. 불일치 값을 자동으로 덮어쓰지 않습니다.

**함수·인자 설명:** json 저장은 ensure_ascii=False·indent=2로 사람이 읽을 수 있게 작성합니다.

실행 위치: 이 README가 있는 폴더. 입력·출력은 파일 위치를 기준으로 찾습니다.

```powershell
python 07_project.py
```

**제작 환경의 실제 실행 출력:**

```text
문서: 5 필드: 15 검토: 2
정답 파일은 추출·검토 판단에 사용하지 않았습니다.
```

**생성 결과:** outputs/final_fields.json, review.csv, doc*_binary.png

**완료 기준:** TODO 구현, 파일 재읽기·수치 확인, 아래 설명을 모두 완료합니다. OCR 버전별 글자·confidence는 달라질 수 있으므로 자신의 결과와 차이를 적습니다.

**설명 질문:** JSON 형식이 맞는 답도 왜 검토가 필요할까요?

내 설명: __________________________________________

## 실습 08 · 같은 프로젝트 재실행 — PPT 85쪽

`07_project.py`를 같은 입력·설정으로 다시 실행합니다. 필드·문서 수와 PNG 크기를 확인합니다. 출력이 다르면 원본·OCR backend·문자 추출 규칙·경로를 점검합니다. 실제 모델이 아닌 경로를 완료라고 과장하지 않습니다.

### 개인 제출·설명

1. 완성 코드와 최종 JSON, 전처리 PNG를 제출합니다.
2. OCR이 읽은 원문과 저장한 필드 값의 차이를 설명합니다.
3. mock VLM 답변과 실제 모델 출력의 차이를 설명합니다.
4. confidence·값 일치·근거 지원이 왜 다른지 설명합니다.
5. 엣지 배포 계획 중 실제로 실행하지 않은 부분을 기록합니다.

기본필수와 응용은 이 README 작성란을 보고서로 사용해도 됩니다.

PSM 비교는 `data/lesson.json`의 실제 기록을 사용합니다. PSM 3·6은 전체 문서, 7은 `total_line.png` 한 줄이므로 서로 다른 대상의 CER로 단순 승자를 고르지 않습니다.
