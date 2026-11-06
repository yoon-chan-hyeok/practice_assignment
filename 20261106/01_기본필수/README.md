# Day15 · 01_기본필수

이 README 하나로 실습 01~08을 진행합니다.

**준비 확인:** 실제 YOLO 실행 파일은 `ultralytics`·`lap` 설치와 강사가 준비한 `data/demo.pt`가 필요합니다. 배포 시 PT는 없습니다. 상위 README의 준비 절차를 먼저 확인하세요.

기본 코드에 사용자 정의 함수·클래스·예외처리를 추가하는 과제가 아닙니다. TODO의 핵심 부분만 작성합니다. 코드가 끝까지 실행돼도 미완성 pass가 남아 있으면 완료가 아닙니다.

## 실습 01 · 이미지·정답 박스 — PPT 15쪽

열 파일: `01_boxes.py` / 직접 완성: **B01**

학습 목표: 해당 처리의 입력·출력을 확인하고, 선택한 좌표·분할·평가 기준을 자신의 말로 설명합니다.

**B01**: 요구: result에 (x1,y1)~(x2,y2) 박스를 두께 2로 그리세요. cv2.rectangle의 이미지·두 점·색은 필수, thickness는 선택입니다.

```powershell
python 01_boxes.py
```

실행 위치: 이 README가 있는 폴더. 전체 경로로 실행해도 입력은 파일 위치를 기준으로 읽습니다.

**함수·인자:** `cv2.imread(filename, flags=cv2.IMREAD_COLOR)`는 경로를 읽어 BGR 배열을 만듭니다. `rectangle(img, pt1, pt2, color, thickness=1)`의 앞 4개는 필수, 두께는 선택입니다. `image.copy()`로 원본과 그릴 배열을 분리합니다.

**확인 출력 — 제작 환경에서 실제 실행**

```text
class: 0 xyxy: 12 18 52 58 GT confidence: N/A
class: 1 xyxy: 70 60 108 98 GT confidence: N/A
class: 2 xyxy: 116 18 150 62 GT confidence: N/A
shape: (128, 160, 3) 저장: p01_boxes.png
```

**완료 기준:** TODO 구현 → 실제 출력/파일 확인 → 아래 설명 작성. 실제 YOLO 미실행은 완료로 표시하지 않습니다.

**설명 질문:** GT에도 confidence가 있는가? 색의 BGR 순서와 xyxy 좌표의 의미는?

내 설명: ______________________________

## 실습 02 · IoU·일대일 매칭 — PPT 27쪽

열 파일: `02_iou.py` / 직접 완성: **B02, B03**

학습 목표: 해당 처리의 입력·출력을 확인하고, 선택한 좌표·분할·평가 기준을 자신의 말로 설명합니다.

**B02**: 요구: intersection을 union으로 나누어 iou를 계산하세요. 이 실습의 데이터는 모두 양의 면적이므로 union은 0이 아닙니다.

**B03**: 요구: 같은 클래스의 미사용 정답에 IoU>=0.5이면 연결하고 used에 기록하세요.

```powershell
python 02_iou.py
```

실행 위치: 이 README가 있는 폴더. 전체 경로로 실행해도 입력은 파일 위치를 기준으로 읽습니다.

**함수·인자:** IoU=교집합/합집합입니다. `np.argsort`는 값 순서의 index, `DataFrame.itertuples()`는 행 묶음을 돌려줍니다. score순 매칭·클래스 일치·정답 한 번 사용을 모두 지켜야 합니다.

**확인 출력 — 제작 환경에서 실제 실행**

```text
class  confidence  max_iou result
     0        0.95   0.9025     TP
     0        0.85   0.8162     FP
     1        0.80   1.0000     TP
     2        0.40   0.0000     FP
TP/FP/FN: 2 2 1
Precision/Recall: 0.5 0.6667
```

**완료 기준:** TODO 구현 → 실제 출력/파일 확인 → 아래 설명 작성. 실제 YOLO 미실행은 완료로 표시하지 않습니다.

**설명 질문:** 같은 정답에 박스 두 개가 겹치면 왜 둘 다 TP가 아닌가? confidence와 IoU는 왜 다른가?

내 설명: ______________________________

## 실습 03 · YOLO 라벨 읽기 — PPT 39쪽

열 파일: `03_labels.py` / 직접 완성: **B04**

학습 목표: 해당 처리의 입력·출력을 확인하고, 선택한 좌표·분할·평가 기준을 자신의 말로 설명합니다.

**B04**: 요구: UTF-8 라벨 파일의 문자열을 읽고 줄 목록으로 나누세요.

```powershell
python 03_labels.py
```

실행 위치: 이 README가 있는 폴더. 전체 경로로 실행해도 입력은 파일 위치를 기준으로 읽습니다.

**함수·인자:** `Path.read_text(encoding="utf-8")`는 문자열, `.splitlines()`는 줄 목록을 반환합니다. 한 줄은 `class cx cy w h`이며 좌표 4개는 0~1 정규화입니다. `shape=(H,W,C)`, 정규화 x/W·y/H를 구분합니다.

**확인 출력 — 제작 환경에서 실제 실행**

```text
basic_train_000.png shape: (128, 160, 3) boxes: 3
  square normalized: 0.796875 0.33984375 0.19375 0.2421875
  circle normalized: 0.1875 0.25 0.1625 0.203125
  triangle normalized: 0.48125 0.640625 0.2125 0.265625
basic_train_001.png shape: (128, 160, 3) boxes: 3
  square normalized: 0.23125 0.234375 0.225 0.28125
  circle normalized: 0.50625 0.6875 0.2 0.25
  triangle normalized: 0.834375 0.27734375 0.23125 0.2890625
basic_train_002.png shape: (128, 160, 3) boxes: 3
  square normalized: 0.165625 0.32421875 0.21875 0.2734375
  circle normalized: 0.79375 0.3046875 0.2 0.25
  triangle normalized: 0.55 0.65625 0.1875 0.234375
basic_train_003.png shape: (128, 160, 3) boxes: 3
  square normalized: 0.83125 0.25 0.175 0.21875
  circle normalized: 0.178125 0.29296875 0.19375 0.2421875
  triangle normalized: 0.534375 0.64453125 0.18125 0.2265625
basic_train_004.png shape: (128, 160, 3) boxes: 3
  square normalized: 0.853125 0.26953125 0.18125 0.2265625
  circle normalized: 0.453125 0.76171875 0.23125 0.2890625
  triangle normalized: 0.215625 0.33984375 0.23125 0.2890625
basic_train_005.png shape: (128, 160, 3) boxes: 3
  square normalized: 0.1625 0.328125 0.1875 0.234375
  circle normalized: 0.846875 0.28515625 0.16875 0.2109375
  triangle normalized: 0.54375 0.734375 0.2 0.25
```

**완료 기준:** TODO 구현 → 실제 출력/파일 확인 → 아래 설명 작성. 실제 YOLO 미실행은 완료로 표시하지 않습니다.

**설명 질문:** width와 height를 바꿔 정규화하면 어떤 문제가 생기는가?

내 설명: ______________________________

## 실습 04 · YOLO 학습 연결 — PPT 53쪽

열 파일: `04_train.py` / 직접 완성: **B05**

학습 목표: 해당 처리의 입력·출력을 확인하고, 선택한 좌표·분할·평가 기준을 자신의 말로 설명합니다.

**B05**: 요구: config_path로 1 epoch, imgsz=160, batch=4, CPU 학습을 호출하세요. 나머지 옵션은 제공한 그대로 유지하세요. test 경로는 전달하지 않습니다.

```powershell
python 04_train.py
```

실행 위치: 이 README가 있는 폴더. 전체 경로로 실행해도 입력은 파일 위치를 기준으로 읽습니다.

**함수·인자:** `YOLO(model=...)`는 구조 YAML 또는 학습된 PT를 받습니다. 생성자에 기본값이 있어도 이 실습에서는 파일을 명시합니다. `.train(**kwargs)`에서 이번 맞춤 데이터의 `data`는 실습상 필수입니다. `epochs/imgsz/batch/device/workers/seed/optimizer`는 선택 설정입니다. CLI도 동일한 값을 지정합니다.

**실제 모델 실행 미검증:** 이 파일은 공식 API를 대조하고 문법만 검사했습니다. 모델 설치·준비 후 직접 실행해 나온 값을 기록하세요. 가상 결과 수치를 정답으로 제공하지 않습니다.

생성할 것: 학습 runs 폴더, results.csv, weights/best.pt·last.pt. 1~2 epoch의 성능이 낮아도 실패라고 단정하지 않습니다.

**완료 기준:** TODO 구현 → 실제 출력/파일 확인 → 아래 설명 작성. 실제 YOLO 미실행은 완료로 표시하지 않습니다.

**설명 질문:** 1 epoch 연결 성공과 실제 탐지 품질이 다른 이유는? `.yaml`과 `.pt`는 무엇이 다른가?

내 설명: ______________________________

## 실습 05 · 학습 기록 해석 — PPT 64쪽

열 파일: `05_metrics.py` / 직접 완성: **B06**

학습 목표: 해당 처리의 입력·출력을 확인하고, 선택한 좌표·분할·평가 기준을 자신의 말로 설명합니다.

**B06**: 요구: map50_95가 가장 큰 행을 선택하세요. idxmax는 첫 최대값의 index를 반환합니다.

```powershell
python 05_metrics.py
```

실행 위치: 이 README가 있는 폴더. 전체 경로로 실행해도 입력은 파일 위치를 기준으로 읽습니다.

**함수·인자:** `Series.idxmax()`는 최대값이 처음 나타나는 행 index, `.loc[index]`는 해당 행을 선택합니다. 여기서는 map50_95 최대를 고릅니다. 실제 Ultralytics best 선택은 라이브러리의 fitness·checkpoint 기록으로 확인합니다.

**확인 출력 — 제작 환경에서 실제 실행**

```text
자료 종류: 읽기 연습용 가상 기록 — 실제 YOLO 성능 아님
선택 epoch: 4
mAP50: 0.55 mAP50-95: 0.27
mAP는 accuracy가 아닙니다. train이 아니라 valid의 위치·분류 평가 기록입니다.
```

**완료 기준:** TODO 구현 → 실제 출력/파일 확인 → 아래 설명 작성. 실제 YOLO 미실행은 완료로 표시하지 않습니다.

**설명 질문:** mAP50-95가 mAP50보다 낮은 이유는? 이 예제 표가 실제 모델 결과인가?

내 설명: ______________________________

## 실습 06 · YOLO 추론 — PPT 75쪽

열 파일: `06_predict.py` / 직접 완성: **B07**

학습 목표: 해당 처리의 입력·출력을 확인하고, 선택한 좌표·분할·평가 기준을 자신의 말로 설명합니다.

**B07**: 요구: data/images/val을 conf=0.25, imgsz=160, CPU로 predict 하세요. source는 입력 경로, conf/imgsz/device는 선택 인자입니다.

```powershell
python 06_predict.py
```

실행 위치: 이 README가 있는 폴더. 전체 경로로 실행해도 입력은 파일 위치를 기준으로 읽습니다.

**함수·인자:** `.predict(source=None, stream=False, **kwargs)`는 기본적으로 Results 목록, `stream=True`면 generator입니다. source는 API 기본값이 있어도 실습에서는 반드시 지정합니다. conf·imgsz·device는 선택입니다. `boxes.xyxy/cls/conf`는 Tensor 속성입니다. `.cpu().tolist()`로 CSV용 값으로 바꿉니다.

**실제 모델 실행 미검증:** 이 파일은 공식 API를 대조하고 문법만 검사했습니다. 모델 설치·준비 후 직접 실행해 나온 값을 기록하세요. 가상 결과 수치를 정답으로 제공하지 않습니다.

생성할 것: 이미지별 탐지 정보 또는 confidence 후보 비교표. 결과가 0개인 입력도 처리한 이미지 수에 포함합니다.

**완료 기준:** TODO 구현 → 실제 출력/파일 확인 → 아래 설명 작성. 실제 YOLO 미실행은 완료로 표시하지 않습니다.

**설명 질문:** 탐지가 0개인 이미지도 결과에 남겨야 하는 이유는? test 대신 val을 쓰는 이유는?

내 설명: ______________________________

## 실습 07 · 탐지·추적 통합 — PPT 86·91쪽

열 파일: `07_project.py` / 직접 완성: **B08, B09**

학습 목표: 해당 처리의 입력·출력을 확인하고, 선택한 좌표·분할·평가 기준을 자신의 말로 설명합니다.

**B08**: 요구: demo.avi를 ByteTrack으로 읽는 stream=True 결과 generator를 만드세요. persist=False는 새로운 파일 스트림의 시작입니다. 같은 파일 내부 프레임은 이어집니다.

**B09**: 요구: tracks를 지정한 열 이름의 CSV로 저장하세요. index=False를 사용합니다.

```powershell
python 07_project.py
```

실행 위치: 이 README가 있는 폴더. 전체 경로로 실행해도 입력은 파일 위치를 기준으로 읽습니다.

**함수·인자:** `.track(source=None, stream=False, persist=False, **kwargs)`는 tracker ID를 포함한 Results를 반환합니다. tracker는 선택 파일명, boxes.id는 아직 ID가 없으면 None일 수 있습니다. OpenCV VideoWriter의 filename·fourcc·fps·frameSize를 지정하고 반드시 release합니다. Track ID는 전 세계 고유 ID가 아닙니다.

**실제 모델 실행 미검증:** 이 파일은 공식 API를 대조하고 문법만 검사했습니다. 모델 설치·준비 후 직접 실행해 나온 값을 기록하세요. 가상 결과 수치를 정답으로 제공하지 않습니다.

생성할 것: 탐지/추적 CSV·프레임 기록·AVI. 정상 입력에서 처리 프레임 수는 30, 입력 FPS는10, 크기는160×128입니다. 탐지 개수·ID·실행시간은 모델과 환경에 따라 달라집니다.

**완료 기준:** TODO 구현 → 실제 출력/파일 확인 → 아래 설명 작성. 실제 YOLO 미실행은 완료로 표시하지 않습니다.

**설명 질문:** ID의 개수와 ID switch는 같은가? 새 영상에 이전 tracker 상태를 붙이면 어떤 문제가 생기는가?

내 설명: ______________________________

## 실습 08 · 같은 프로젝트 재실행 — PPT 91쪽
`07_project.py`를 설정 변경 없이 다시 실행합니다. CSV의 행·이미지·프레임 수, 영상의 해상도·FPS를 대조하세요.
서로 다른 device/라이브러리에서 동일한 시간이나 완전한 bitwise 예측을 요구하지 않습니다. 0개 검출과 파일 저장 실패를 구분합니다.
제출: 완성한 Python 파일, 생성 결과, 이 README에 작성한 설명. 기본필수는 Git 명령·보고서 모듈·별도 테스트 작성을 추가하지 않습니다.

### 설명 3문장
1. 좌표와 라벨을 어떻게 확인했는가? __________________
2. 실제 모델이 놓친 것/중복한 것과 측정한 한계는? __________________
3. 다음 개선 때 고정할 분할·conf·tracker·입력·모델 버전은? __________________
