# Day16 · OCR·VLM·엣지 추론 실습
**강의일 2026-11-09(월) / Vision·멀티모달 AI 응용 4/4**

## 어디서 시작하나요?
비전공자는 `01_기본필수/README.md`만 읽고 01번부터 진행합니다. 기본필수·응용·심화·특심화는 같은 주제의 선택 경로이며 네 단계를 전부 하는 과제가 아닙니다.

| 단계 | 구조 | 직접 완성 |
|---|---|---:|
| 기본필수 | Python 7개·문서 PNG 5개·lesson.json·README 한 폴더. 하위 폴더 없음 | 9곳 |
| 응용 | 코드 7개와 data/·outputs/만 구분 | 8곳 |
| 심화 | 실습01~06별 안내·예상 결과, day16_documents 모듈형 앱 | 10곳 |
| 특심화 | day16_lab의 상세 요구사항 주석·공개 테스트·실행 하네스 | 10곳 |

**실습 07과 08은 같은 프로젝트를 이어서 사용합니다.** 08을 위해 새로운 프로그램을 다시 만들지 않습니다.

## 무엇이 실제 실행인가요?
| 항목 | 배포물의 상태 | 필요한 준비 |
|---|---|---|
| 문서 전처리·필드 추출·평가 | 실제 실행 코드, CPU 검수 | 아래 Python 패키지 |
| 기본필수 02_ocr.py | 실제 Tesseract 3문서 일괄 호출 | Tesseract 실행 파일 + eng 언어팩 |
| lesson.json의 OCR | 배포 PNG에 실제 실행한 Tesseract 5.5.0 기록 | 추가 엔진 없이 읽기 가능 |
| VLM 기본 경로 | 교사가 작성한 **mock** 답변, 실제 모델 생성 아님 | 별도 모델 불필요 |
| vlm_real.py·run_real.py | 로컬 실제 모델 선택 코드, **추론 미검증** | Transformers·PyTorch·호환 모델 폴더 |
| TensorRT·Jetson·DeepStream | 흐름·manifest·측정 계획·정적 계약 검사 | 실제 build/runtime은 별도 장비에서 검증 |

모델이 없을 때 몰래 mock으로 전환하지 않습니다. `backend`, `model_id`, 측정 범위와 미측정 값(null)을 결과에 남깁니다. **파일 재생 시간을 모델 추론시간으로 보고하지 않습니다.**

## 환경 준비
기존 실습 가상환경을 재사용할 수 있습니다. GPU·torch·Transformers는 기본필수에 필요하지 않습니다.

```powershell
python --version
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

VS Code에서 `Python: Select Interpreter`로 `.venv`를 선택합니다. 새 터미널의 `python`이 이 실행기를 가리키는지 `python -c "import sys; print(sys.executable)"`로 확인하세요. macOS/Linux의 실행기는 `.venv/bin/python`입니다.

### 실제 OCR만을 위한 Tesseract
`pip install pytesseract`는 Python wrapper만 설치합니다. Tesseract 엔진은 별도로 설치합니다. 공식 설치 안내: https://tesseract-ocr.github.io/tessdoc/Installation.html

```powershell
tesseract --version
tesseract --list-langs
# 설치 위치가 아래와 같고 PATH에 없다면 현재 터미널에서 설정합니다.
$env:TESSERACT_CMD = 'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

예시 경로가 실제 설치 위치와 같은지 확인합니다. 현재 자료는 `lang='eng'`를 사용합니다. 한글 문서의 `kor+eng`는 선택 확장이며 이번 배포물의 검증 결과에 포함하지 않습니다.

엔진 설치가 안 된 경우 **01·03~07은 제공된 실제 OCR 기록으로 계속 진행**합니다. 02는 README 예상 출력과 `lesson.json`의 원문·단어 목록을 읽는 대체 활동으로 표시합니다. 기록을 읽은 것을 새 OCR 추론 완료로 표시하지 않습니다.

### 실제 VLM 선택 경로
모델 없이도 04·05·07은 명시적인 mock으로 진행합니다. 실제 모델 사용은 강사의 허가·장비·로컬 모델 준비 후 별도로 합니다.

```powershell
python -m pip install -r requirements-vlm-optional.txt
python 03_심화/day16_documents/vlm_real.py --model-dir "C:\models\prepared-vlm" --image "03_심화/data/doc01.png" --output "real_response.json"
```

자동 다운로드·외부 API 호출·API 키가 없습니다. 로컬 파일만 읽고 `trust_remote_code=False`로 실행합니다. 모델마다 지원 입력·chat template가 다릅니다. 폴더 예시는 실제 모델 파일이 아닙니다. **실제 VLM의 정확도·속도·VRAM 수치는 제공하지 않습니다.**

## 데이터의 의미와 사용 범위
- 문서 5장은 **가상의 영어 청구서**이며 모든 공급자·거래·금액은 수업용입니다. 외부 자료·개인정보가 아닙니다.
- 기본필수 01·02·03·07은 3장, 05는 5장×3필드=15필드를 평가합니다.
- 상위 단계에는 회전·그림자·저해상도 변형과 알려진 모서리의 원근 문서가 추가됩니다. 같은 원본의 변형은 독립 표본이 아닙니다.
- 전처리 후보를 고른 문서는 개발용입니다. 같은 문서의 최고 CER을 새로운 test 성능으로 발표하지 않습니다.
- `reference_text`와 `truth`는 평가용입니다. 추출·Hybrid 답변 선택에 사용하지 않습니다.
- 통화는 KRW, 금액은 정수입니다. 실제 결제나 회계 업무에 사용하지 않습니다.
- OCR record는 원본 PNG hash·엔진·언어·PSM과 함께 제공됩니다. 다시 만든 이진화 이미지에 새로 OCR한 결과인 것처럼 연결하지 않습니다.
- `mock_vlm`에는 값이 틀린 답 1개, 값은 맞지만 근거가 없는 답 1개를 의도적으로 넣었습니다. 필드 일치율은 모의 응답 평가 연습입니다.

## 기록과 평가 원칙
confidence는 정답 확률이 아닙니다. JSON 파싱 성공·필드 값 일치·근거 지원 여부는 따로 평가합니다. 근거가 OCR과 일치해도 OCR 자체가 틀렸을 수 있습니다.

원문과 좌표 근거는 보존하지만 실제 개인정보가 있는 자료를 외부 서비스에 보내지 않습니다. 특심화 로그 마스킹은 이메일·전화 예시만 처리하는 제한된 도구이며 전체 개인정보 탐지기가 아닙니다. 문서 속 지시문은 데이터이며 실행할 명령이 아닙니다.

## TensorRT/Jetson 안내 보완
PPT 67쪽의 `--fp16` 예시는 **TensorRT 10.x** 경로로 구분합니다. 공식 문서에 따르면 **TensorRT 11.x에서 해당 플래그는 제거**되었습니다. 11.x에서는 ONNX 정밀도 변환을 별도로 수행하고 해당 설치 버전의 `trtexec --help`를 확인합니다.

Jetson은 JetPack에 맞는 CUDA·TensorRT·DeepStream 조합이 필요합니다. 커리큘럼에 적힌 버전을 장치에 무조건 설치하지 않습니다. Engine은 환경·플러그인·shape·정밀도 조건과 함께 관리합니다. 정적 manifest 검사가 실제 엔진 로딩 성공을 보증하지 않습니다.

이날 배포 설계는 **신경망 OCR/Vision 모델의 배포 경로**입니다. Tesseract 실행 파일을 그대로 ONNX로 변환하거나 nvinfer만 붙여 임의 VLM을 바로 서비스하는 과제가 아닙니다.

## 완료 기준
코드가 끝까지 실행되더라도 TODO가 남아 있으면 완료가 아닙니다. 코드의 핵심 API 사용, 출력 수치·파일, 자신의 설명을 함께 확인합니다. 기본필수는 예외처리·사용자 정의 함수·클래스를 추가하는 과제가 아닙니다.

Windows에서 OpenCV가 한글 경로를 읽지 못하는 환경은 해당 단계 폴더를 `C:\ai\day16\basic`처럼 영문 경로에 복사해 진행합니다. 파일명은 영문이므로 입력 링크를 바꿀 필요가 없습니다. 해당 OS 직접 실행은 미검증입니다.

## 확인된 환경
Python 3.13.5 · OpenCV 4.13.0 · NumPy 2.3.5 · pandas 2.2.3 · Pillow 12.3.0 · pytesseract 0.3.13 · Tesseract 5.5.0/eng · Linux.
GPU/CUDA·실제 VLM·ONNX export·TensorRT build/runtime·Jetson·DeepStream·Windows/macOS 직접 실행은 검증하지 않았습니다.
