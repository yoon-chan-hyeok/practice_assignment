# Day16 · 01_기본필수 · 수강생용

이 README 하나로 실습 01~08을 진행합니다. 전체 환경 준비는 상위 `README.md`를 읽습니다.

기본필수는 정상 데이터·제공 골격의 핵심만 완성합니다. 함수·클래스·예외처리를 추가하지 않습니다.

**실제 OCR:** 기본필수 02는 Tesseract+eng가 필요합니다. 다른 파일은 제공 OCR 기록으로 독립 실행됩니다. VLM은 mock, 배포는 설계입니다.

## 실습 01 · 문서 전처리 — PPT 19쪽

**목표:** Gray·이진화의 모양과 출력을 확인합니다.

**열 파일:** `01_preprocess.py`

**B01 요구사항:** BGR를 Gray로 변환한 뒤 Otsu 이진화를 호출하세요. threshold는 자동으로 구한 숫자, binary는 결과 배열입니다.

**함수·인자 설명:** cvtColor(src, code): 둘 다 필수. threshold(src, thresh, maxval, type): 앞 4개 필수, (실제 임계값, 결과)를 반환합니다.

실행 위치: 이 README가 있는 폴더. 입력·출력은 파일 위치를 기준으로 찾습니다.

```powershell
python 01_preprocess.py
```

**제작 환경의 실제 실행 출력:**

```text
doc01 shape: (700, 1000) threshold: 145.0
doc02 shape: (700, 1000) threshold: 145.0
doc03 shape: (700, 1000) threshold: 145.0
```

**생성 결과:** p01_*.png 6개

**완료 기준:** TODO 구현, 파일 재읽기·수치 확인, 아래 설명을 모두 완료합니다. OCR 버전별 글자·confidence는 달라질 수 있으므로 자신의 결과와 차이를 적습니다.

**설명 질문:** 이진화 후 눈으로 읽기 쉬워지면 OCR 정확도도 반드시 높아질까요?

내 설명: __________________________________________

## 실습 02 · 실제 OCR 실행 — PPT 29쪽

**목표:** 3문서의 문자열·단어 수·평균 신뢰도를 확인합니다.

**열 파일:** `02_ocr.py`

**B02 요구사항:** image_to_data를 호출해 단어·좌표·confidence가 포함된 표를 받으세요. lang=eng, config=--psm 6, output_type=Output.DATAFRAME을 사용합니다.

**함수·인자 설명:** image_to_data(image, lang=None, config="", output_type=Output.STRING): image 필수, 나머지 선택. 엔진 실행 파일은 pip 패키지와 별개입니다.

실행 위치: 이 README가 있는 폴더. 입력·출력은 파일 위치를 기준으로 찾습니다.

```powershell
python 02_ocr.py
```

**제작 환경의 실제 실행 출력:**

```text
page: 1 words: 27 mean confidence: 95.44
INVOICE DOCO1 DATE: 2026-11-01 SUPPLIER: BLUE CAFE ITEM QTY PRICE AMOUNT TEA 2 3000 6000 COFFEE 3 5000 15000 CAKE 1 6000 6000 TOTAL: 27000 CURRENCY: KRW
page: 2 words: 27 mean confidence: 95.13
INVOICE DOCO2 DATE: 2026-11-02 SUPPLIER: PINE BOOKS ITEM QTY PRICE AMOUNT BOOK 2 6000 12000 PEN 3 1000 3000 PAD 1 3000 3000 TOTAL: 18000 CURRENCY: KRW
page: 3 words: 27 mean confidence: 94.55
INVOICE DOCO3 DATE: 2026-11-03 SUPPLIER: ALPHA STUDIO ITEM QTY PRICE AMOUNT PRINT 4 3000 12000 FRAME 1 9000 9000 PAPER 3 4000 12000 TOTAL: 33000 CURRENCY: KRW
backend: live Tesseract; confidence는 정답 확률이 아닙니다.
```

**생성 결과:** p02_inputs.txt, p02_words.csv

**완료 기준:** TODO 구현, 파일 재읽기·수치 확인, 아래 설명을 모두 완료합니다. OCR 버전별 글자·confidence는 달라질 수 있으므로 자신의 결과와 차이를 적습니다.

**설명 질문:** confidence 95가 문자와 업무 의미가 95% 정확하다는 뜻일까요?

내 설명: __________________________________________

## 실습 03 · 필드 JSON — PPT 39쪽

**목표:** 날짜·공급자·합계를 추출하고 원문과 함께 저장합니다.

**열 파일:** `03_fields.py`

**B03 요구사항:** DATE:로 시작하는 줄의 날짜를 group(1)로 꺼내세요. 이 정상 데이터에는 날짜 줄이 존재합니다.

**B04 요구사항:** TOTAL: 줄의 숫자를 꺼내 int로 변환하세요. 전체 문자열에서 첫 숫자를 가져오지 않습니다.

**함수·인자 설명:** re.search(pattern, string, flags=0): 앞 두 인자 필수. group(1)은 첫 괄호 그룹. json.dumps(obj, ensure_ascii=True, indent=None): obj 필수, 나머지 선택입니다.

실행 위치: 이 README가 있는 폴더. 입력·출력은 파일 위치를 기준으로 찾습니다.

```powershell
python 03_fields.py
```

**제작 환경의 실제 실행 출력:**

```text
doc01 2026-11-01 BLUE CAFE 27000
doc02 2026-11-02 PINE BOOKS 18000
doc03 2026-11-03 ALPHA STUDIO 33000
```

**생성 결과:** p03_fields.json

**완료 기준:** TODO 구현, 파일 재읽기·수치 확인, 아래 설명을 모두 완료합니다. OCR 버전별 글자·confidence는 달라질 수 있으므로 자신의 결과와 차이를 적습니다.

**설명 질문:** 첫 번째 숫자를 합계라고 읽으면 무엇이 잘못될까요?

내 설명: __________________________________________

## 실습 04 · VLM 메시지와 모의 응답 — PPT 52쪽

**목표:** 모델 없이 멀티모달 메시지 구조를 익힙니다.

**열 파일:** `04_messages.py`

**B05 요구사항:** role=user, content 안에 image/path와 text/text 항목을 넣으세요. 파일을 저장하는 것과 VLM 추론은 다릅니다.

**함수·인자 설명:** content는 image·text 사전의 목록입니다. 이 파일에서는 generate나 외부 API를 호출하지 않습니다.

실행 위치: 이 README가 있는 폴더. 입력·출력은 파일 위치를 기준으로 찾습니다.

```powershell
python 04_messages.py
```

**제작 환경의 실제 실행 출력:**

```text
What is the issue date? -> 2026-11-01
Who is the supplier? -> BLUE CAFE
What is the total in KRW? -> 27000
MOCK: 교사가 작성한 응답 예시입니다. 실제 모델 출력이 아닙니다.
```

**생성 결과:** p04_mock_answers.json

**완료 기준:** TODO 구현, 파일 재읽기·수치 확인, 아래 설명을 모두 완료합니다. OCR 버전별 글자·confidence는 달라질 수 있으므로 자신의 결과와 차이를 적습니다.

**설명 질문:** 이 파일만 실행했을 때 모델 정확도나 GPU 처리시간을 보고해도 될까요?

내 설명: __________________________________________

## 실습 05 · 필드 정확도 — PPT 62쪽

**목표:** 15개 필드의 분모와 일치 개수를 확인합니다.

**열 파일:** `05_evaluate.py`

**B06 요구사항:** 추출값과 해당 필드의 정답을 비교하세요. True/False 값을 correct에 저장합니다.

**함수·인자 설명:** DataFrame(rows)는 사전 목록을 표로 만듭니다. to_csv(path, index=False)는 인덱스를 제외해 저장합니다.

실행 위치: 이 README가 있는 폴더. 입력·출력은 파일 위치를 기준으로 찾습니다.

```powershell
python 05_evaluate.py
```

**제작 환경의 실제 실행 출력:**

```text
문서 수: 5 필드 수: 15
필드 일치: 15 / 15
합성 영어 문서의 기록 비교이며 일반 OCR·한국어 성능이 아닙니다.
```

**생성 결과:** p05_field_scores.csv

**완료 기준:** TODO 구현, 파일 재읽기·수치 확인, 아래 설명을 모두 완료합니다. OCR 버전별 글자·confidence는 달라질 수 있으므로 자신의 결과와 차이를 적습니다.

**설명 질문:** 필드 15개 중 15개가 맞으면 문서 전체 글자도 전부 맞을까요?

내 설명: __________________________________________

## 실습 06 · 배포 흐름 기록 — PPT 73쪽

**목표:** 모델 파일·엔진 빌드·실행을 구분합니다.

**열 파일:** `06_deployment.py`

**B07 요구사항:** 모델 → ONNX 내보내기/검증 → 대상 장치에서 엔진 build → Runtime 추론/검증의 순서를 목록으로 적으세요.

**함수·인자 설명:** json의 null은 Python None입니다. 실제로 측정하지 않은 시간은 0이 아니라 None으로 둡니다.

실행 위치: 이 README가 있는 폴더. 입력·출력은 파일 위치를 기준으로 찾습니다.

```powershell
python 06_deployment.py
```

**제작 환경의 실제 실행 출력:**

```text
PyTorch model -> ONNX export and verify -> TensorRT build on target -> Runtime inference and verify
DESIGN_ONLY: 오늘은 설계 기록. Tesseract 자체를 ONNX로 변환하는 예제가 아닙니다.
```

**생성 결과:** p06_deployment_plan.json

**완료 기준:** TODO 구현, 파일 재읽기·수치 확인, 아래 설명을 모두 완료합니다. OCR 버전별 글자·confidence는 달라질 수 있으므로 자신의 결과와 차이를 적습니다.

**설명 질문:** Tesseract OCR 문자열을 그대로 TensorRT 엔진으로 만들 수 있을까요?

내 설명: __________________________________________

## 실습 07 · OCR 미니 프로젝트 — PPT 83쪽

**목표:** 3문서 전처리·OCR 기록 읽기·필드 저장을 연결합니다.

**열 파일:** `07_project.py`

**B08 요구사항:** 원본 BGR에서 Gray를 만드세요. 원본 파일은 덮어쓰지 않습니다.

**B09 요구사항:** records를 UTF-8 JSON으로 p07_documents.json에 저장하세요. 원문·출처를 제거하지 않습니다.

**함수·인자 설명:** read_text(encoding=...), write_text(data, encoding=...)를 사용합니다. JSON 직렬화와 OCR 추론은 다른 단계입니다.

실행 위치: 이 README가 있는 폴더. 입력·출력은 파일 위치를 기준으로 찾습니다.

```powershell
python 07_project.py
```

**제작 환경의 실제 실행 출력:**

```text
doc01 {'issued_at': '2026-11-01', 'supplier': 'BLUE CAFE', 'total_amount': 27000}
doc02 {'issued_at': '2026-11-02', 'supplier': 'PINE BOOKS', 'total_amount': 18000}
doc03 {'issued_at': '2026-11-03', 'supplier': 'ALPHA STUDIO', 'total_amount': 33000}
문서: 3 / 이진화 PNG 3개 + 최종 JSON 1개
```

**생성 결과:** p07_*_binary.png 3개, p07_documents.json

**완료 기준:** TODO 구현, 파일 재읽기·수치 확인, 아래 설명을 모두 완료합니다. OCR 버전별 글자·confidence는 달라질 수 있으므로 자신의 결과와 차이를 적습니다.

**설명 질문:** 실시간 OCR과 기록 재생은 무엇이 다르며 이번 결과는 어떤 경로인가요?

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
