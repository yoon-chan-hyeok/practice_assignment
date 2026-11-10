# Day15 · 실시간 YOLO 탐지와 결과 분석

**대상:** 기존 Day15 이미지 탐지·IoU·NMS·학습/검증 실습을 마친 수강생  
**핵심:** 처음부터 구현하지 않고 완성 코드로 실행·실험·기록한다.  
**필수:** 웹캠 추론과 결과보고서 / **선택:** 새 데이터셋 추가 학습·정량 평가.

빠른 실행은 **START_HERE.md**를 보세요. 기본 과제를 위해 데이터셋을 다운로드하거나 새로 학습할 필요는 없습니다. 최초 모델 가중치 다운로드와 패키지 설치는 필요합니다.

## 1. 무엇이 다른가?

기존 `day15_detection.zip`은 도형 데이터와 별도 준비한 탐지 모델을 사용하는 프로젝트입니다. 이번 프로젝트는 그 파일을 덮어쓰거나 import하지 않는 **독립 프로젝트**입니다.

기본 모델은 사전학습된 `yolo26n.pt`입니다. 모델 구조만 생성하는 `yolo26n.yaml`이나 2 Epoch smoke 학습 결과로 시작하지 않습니다. 실습 코드에서는 `model.predict()`만 호출하므로 실행할 때마다 모델이 학습되거나 가중치가 바뀌지 않습니다. [1][2]

기본 모델의 클래스 목록은 로딩한 `model.names`가 기준입니다. `check_setup.py` 실행 후 `weights/classes.json`에서도 확인할 수 있습니다. 기존 도형 클래스 `square/circle/triangle` 또는 새 사용자의 고유 물체를 무조건 탐지하는 모델이 아닙니다. [1][3]

## 2. 폴더 구조

```text
day15_realtime_yolo/
├── START_HERE.md               # 수강생은 이것부터
├── main.py                     # 카메라/영상 → 탐지 → 표시 → 증빙/로그
├── config.yaml                 # 기본 모델/카메라/입력 크기/conf/device
├── runtime.py                  # 공통 경로·장치·파일 처리
├── check_setup.py              # 설치/가중치/빈 이미지 추론 사전 점검
├── check_dataset.py            # 선택: 학습용 이미지/라벨 점검
├── train_custom.py             # 선택: 새 데이터 추가 학습
├── evaluate_custom.py          # 선택: 라벨 기반 val 평가
├── requirements.txt
├── weights/                    # 최초 실행 후 yolo26n.pt 저장
├── assets/day15_demo.avi        # 사용자 제공 도형 영상, 입출력 확인용
├── datasets/custom/
│   ├── data.yaml               # 실제 클래스명으로 수정할 템플릿
│   ├── README.md
│   ├── images/{train,val,test}/
│   └── labels/{train,val,test}/
├── reports/
│   ├── REPORT_TEMPLATE.md      # 기본 제출 양식
│   ├── OPTIONAL_REPORT.md      # 추가 학습을 한 경우만 작성
│   └── WRITING_EXAMPLE.md      # 관찰/해석/한계를 구분하는 작성 예
├── docs/
│   ├── TEACHER_GUIDE.md         # 60분 운영안과 평가 기준
│   ├── TROUBLESHOOTING.md
│   └── TESTING.md              # 제작 환경에서 확인한 것/미확인한 것
├── tests/test_offline.py       # 오프라인 로직 점검, 실제 탐지 성능 테스트 아님
└── outputs/                    # 실행마다 새 하위 폴더 생성
```

## 3. 설치·시작

기존 수업용 Python 가상환경을 사용하세요. 터미널의 Python과 VS Code 인터프리터를 일치시킵니다.

```powershell
python -c "import sys; print(sys.executable)"
python -m pip install -r requirements.txt
python check_setup.py --camera 0
python main.py
```

프로젝트 코드는 Python 3.10 이상 문법을 사용합니다. 기존 GPU용 PyTorch가 정상 작동한다면 재설치하지 않습니다. `requirements.txt`는 YOLO26을 지원하는 Ultralytics 8.4 계열 이상/9 미만을 요구하며, 버전 고정 검증 파일은 아닙니다. 수업 환경에서 먼저 점검한 뒤 `python -m pip freeze > environment.txt`로 실제 환경을 기록하세요. Ultralytics 설치 및 GPU용 PyTorch 구성은 공식 설치 안내를 참고합니다. [4]

**가중치 파일은 이 ZIP에 없습니다.** `check_setup.py` 또는 최초 `main.py`에서 공식 가중치를 다운로드합니다. 이후 로컬 파일을 재사용합니다. 인터넷이 차단된 수업장에서는 강사가 사전 준비한 공식 파일을 `weights/yolo26n.pt`에 놓으세요. 불명확한 출처의 `.pt`는 실행하지 않습니다. [4]

## 4. 기본 실행과 설정

```powershell
python main.py
python main.py --conf 0.60
python main.py --source 1
python main.py --device cpu
python main.py --imgsz 640
python main.py --source "C:/videos/my_objects.mp4"
```

| 설정 | 기본값 | 의미 |
|---|---|---|
| source | 0 | 첫 번째 카메라. 문자열 경로는 로컬 영상 |
| conf | 0.25 | 표시할 탐지의 confidence 임계값; 정확도 아님 |
| imgsz | 320 | 모델 입력 기준 크기. 비율 유지/패딩과 실제 내부 크기는 라이브러리가 처리 |
| device | auto | CUDA 사용 가능 시 GPU 0, 아니면 CPU |
| camera_width/height | 640/480 | 카메라에 요청하는 크기. 실제 값은 장치별로 다를 수 있음 |
| model | weights/yolo26n.pt | 기본 사전학습 모델 |

추론은 프레임 한 장씩 처리하여 모든 영상 프레임을 메모리에 쌓아 두지 않습니다. OpenCV 프레임(BGR 배열)을 `predict()`에 전달하고 결과의 `plot()`으로 박스를 그립니다. [2]

영상 창에서 **S**를 누르면 원본과 박스가 있는 화면을 같이 저장합니다. **Q/ESC** 또는 창 닫기로 종료합니다. 기본적으로 녹화는 하지 않습니다. 일괄 캡처는 `--snapshot-every 30`, 종료 프레임 제한은 `--max-frames 100`이며 기본 필수 과제에는 필요하지 않습니다.

원본 프레임은 `snapshots/*_raw.png`로 보존합니다. 개인정보가 있으면 삭제/가림 처리 후 제출하세요. 학습 데이터로 재활용하려면 별도 라벨링과 분할 설계가 필요하며, 카메라의 연속 프레임을 train/val에 무작위로 섞지 마세요.

## 5. 로그의 정확한 의미

```text
outputs/webcam_YYYYMMDD_HHMMSS_xxxxxx/
├── summary.json        # 설정, 장치, 모델 해시, 버전, 처리시간 요약
├── frames.csv          # 탐지 0건인 프레임도 포함
├── detections.csv      # 프레임별 박스/클래스/confidence
├── snapshots.csv       # 캡처 증빙 목록
└── snapshots/
    ├── frame_000042_raw.png
    └── frame_000042_annotated.png
```

| 필드 | 보고서에서의 해석 |
|---|---|
| processed_frames | 처리한 프레임 수 |
| frames_with_detections | 하나 이상의 박스가 나온 프레임 수. 성공률/정확도가 아님 |
| total_detection_rows | 전체 프레임의 박스 수 합계. 서로 다른 실제 객체 수가 아님 |
| predict_call_mean_ms | `model.predict()` 호출 평균 경과시간. 전처리·추론·후처리 포함 |
| predict_call_p95_ms | 측정된 호출 시간의 95백분위수 |
| loop_fps | 프레임 읽기·추론·그리기·표시·탐지행 기록·선택 캡처를 포함하는 처리 루프 FPS |
| run_seconds | 카메라 열기/워밍업/루프를 포함한 실행 시간. 모델 최초 로딩은 제외 |
| accuracy / map50_95 | 기본 실습에서는 `null`, 즉 미측정 |

워밍업 2회는 predict/loop 통계에서 제외합니다. `loop_fps`에서 최초 준비·마지막 요약·`frames.csv` 행 쓰기는 제외하고, 첫 프레임은 준비 단계에서 읽습니다. FPS는 카메라 스펙, 화면에 보이는 지연의 역수 또는 순수 신경망 처리량이 아닙니다. 장면·장치·표시·저장 여부가 바뀌면 값도 바뀝니다. 로그의 정의를 유지하여 비교하세요.

## 6. 필수 보고서 제출

`reports/REPORT_TEMPLATE.md`를 `reports/REPORT_이름.md`로 복사합니다. 기본 조건과 변경 조건의 실행 폴더를 각각 적고 캡처 2장 이상을 근거로 씁니다. 관찰 범위에서 오류가 없다면 그대로 기록합니다.

정답 라벨 없이 **confidence 평균을 Accuracy로 쓰지 않습니다.** 검출 박스가 많이 나오는 것이 곧 성능이 좋은 것도 아닙니다. 웹캠 관찰은 정성 평가이며, mAP는 정답 라벨이 있는 별도 평가에서 계산합니다. [5]

## 7. 선택: 새 데이터로 학습·평가·웹캠 적용

`datasets/custom/README.md`의 폴더/라벨 안내를 먼저 읽습니다.

```powershell
python check_dataset.py
python train_custom.py --epochs 2 --imgsz 320 --batch 4
python evaluate_custom.py
python main.py --model custom
```

2 Epoch는 연결 확인용 예시입니다. 성능 향상이나 수업 내 완료를 보장하지 않습니다. `--epochs 5` 등으로 늘리거나 `--device cpu`를 명시할 수 있습니다. 새 학습의 기본 `epochs`는 5입니다. 학습을 마치면 `outputs/train_.../weights/best.pt`와 `last.pt`가 만들어집니다. 이 프로젝트는 완료된 가장 최근 학습을 `outputs/latest_custom.json`에 기록하여 `--model custom`으로 사용합니다. [6]

`evaluate_custom.py`는 기본적으로 **val만 평가**합니다. 실제 검증된 클래스만 `class_metrics.csv`에 기록합니다. Test는 새 데이터의 YAML에 test 경로를 명시하고, 실험 설계를 고정한 최종 평가 때 `--split test`로만 사용합니다. [5]

모델 클래스와 YAML의 클래스 이름/순서가 다르면 평가를 중단합니다. COCO 기본 모델과 사용자 2클래스 모델의 ID를 그대로 맞춰 mAP를 비교하지 마세요. 새로운 학습 후 모든 COCO 클래스에 새 클래스가 단순히 추가되는 것도 아닙니다.

## 8. 확인 범위와 출처

제작 환경의 검증 범위는 `docs/TESTING.md`를 보세요. 실제 웹캠 화면, CUDA, YOLO 가중치 추론/추가 학습은 수업 장비에서 `check_setup.py`와 기본 실행으로 확인해야 합니다.

- [1] 공식 YOLO26 모델 안내: https://docs.ultralytics.com/models/yolo26/
- [2] 예측 API, OpenCV 배열 입력, 결과 객체: https://docs.ultralytics.com/modes/predict/
- [3] 객체 탐지 데이터 형식과 COCO 클래스 예시: https://docs.ultralytics.com/datasets/detect/
- [4] 설치 및 자동 가중치 다운로드: https://docs.ultralytics.com/quickstart/
- [5] Validation 지표·설정: https://docs.ultralytics.com/modes/val/
- [6] 학습 API, checkpoint, Windows 진입점: https://docs.ultralytics.com/modes/train/

문서 확인일: 2026-11-06. 공식 라이브러리는 변경될 수 있으므로 실제 실행 버전도 보고서에 남기세요. 위 문서들의 내용을 그대로 옮긴 자료가 아니라 본 실습의 구현과 사용 안내입니다.
