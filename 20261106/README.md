# Day15 · 객체탐지·IoU·YOLO 학습·추론·추적
2026년 11월 6일(금) / 강의 원본: `Day15_ObjectDetection_YOLO_Tracking_20261106.pptx`

## 먼저 확인 — 실제 YOLO 실습에는 교실 사전 준비가 필요합니다
**제작 환경에서 Ultralytics와 lap 다운로드가 실패했습니다. 실제 YOLO 학습·검증·추론·추적·resume는 실행 미검증입니다.**
소스는 공식 API를 대조하고 문법을 검사했지만, 그것을 실제 모델 실행 통과로 표시하지 않았습니다.
배포 ZIP에는 `data/demo.pt`가 없습니다. 강사가 아래 준비 절차로 모델을 학습·복사한 뒤 학생용을 배포하세요.

좌표·IoU·라벨·교육용 AP·매칭·원리 추적기·artifact 재개 테스트는 실행 검수했습니다. 그 결과를 YOLO 성능이라고 부르지 않습니다.
`boxes_fixture.csv`와 `metrics_example.csv`는 **손으로 정한 원리/표 읽기 예시**입니다. 실제 학습 기록이 아닙니다.

## 학습 경로
| 단계 | 폴더 | 직접 구현 | 구조 |
|---|---|---:|---|
| 기본필수 | `01_기본필수/` | 9곳 | Python 7개·README + YOLO에 필요한 data 구조 |
| 응용 | `02_응용/` | 8곳 | 코드 + data/ + outputs/ |
| 심화 | `03_심화/` | 10곳 | 실습별 README·expected + 모듈형 프로젝트 |
| 특심화 | `04_특심화/day15_lab/` | 10곳 | 계약·모듈·공개 테스트·상세 주석 |

네 단계를 전부 푸는 일정이 아닙니다. 기본필수를 먼저 완료하고 응용·심화·특심화 중 적절한 경로를 선택하세요.
기본필수·응용의 `pass`는 미완성 표시입니다. 실행 종료만으로 완료가 아닙니다. 코드와 결과를 함께 확인합니다.
특심화의 `NotImplementedError`는 구현할 함수라는 뜻입니다. 테스트 실패를 무시하고 통과로 기록하지 마세요.

## 설치
기존 Day9~14의 Python 가상환경·torch·torchvision을 유지합니다. CUDA를 위해 임의 버전의 torch를 다시 설치하지 않습니다.
VS Code의 Python 실행기를 그 환경으로 선택한 뒤, 이 README가 있는 역할 폴더에서 실행합니다.

```powershell
python -m pip install -r requirements.txt
python -c "import torch, torchvision, cv2, ultralytics, lap; print(torch.__version__, torchvision.__version__, cv2.__version__, ultralytics.__version__)"
```

`ultralytics==8.4.21`, `lap==0.5.12`는 **실행 대상 버전이지 제작 환경의 실행 검증 버전은 아닙니다.** 설치 가능한 공식 배포본임을 확인했지만 여기서는 설치되지 않았습니다.
기존 CPU 검수 환경: Python 3.13.5, torch 2.10.0+cpu, torchvision 0.25.0+cpu, OpenCV 4.13.0, NumPy 2.3.5, pandas 2.2.3.
GPU, Windows/macOS, 실제 YOLO, 다른 OpenCV 영상 backend는 교실에서 확인해야 합니다.

## 강사의 한 번 사전 준비
전체 ZIP을 풀어 강사용과 수강생용이 보이는 위치에서 실행합니다.

```powershell
python "강사용/운영/prepare_yolo.py" --student-root "수강생용" --epochs 60 --device cpu
python "강사용/운영/verify_yolo_ready.py" --root "수강생용"
```

CUDA가 준비된 교실에서는 첫 명령의 `--device 0`을 사용할 수 있습니다. 실제 학습 결과와 모델 품질은 반드시 확인하세요.
기본 명령은 설치 패키지의 `yolo26n.yaml` 구조에서 **별도 source 도형 데이터**로 학습합니다. 외부 COCO weight 다운로드가 없어도 됩니다.
`--init yolo26n.pt`는 공식 COCO weight를 추가로 내려받아 시작하는 선택 경로입니다. 인터넷/라이선스 확인이 필요합니다.
준비 도구는 자체 생성한 best.pt를 각 단계의 `data/demo.pt`로 복사하고 해시·출처·실제 `source_results_actual.csv`를 기록합니다.
준비 후 학생용을 재압축하려면 `--out-zip Day15_ready_student.zip`을 첫 명령에 추가합니다. **준비 전에 받은 학생용 ZIP에는 모델이 없습니다.**

실패할 경우 무작위 모델이나 손계산 box를 실제 YOLO 예측으로 자동 대체하지 않습니다.
모델 준비가 끝나기 전에는 기본필수 01·02·03·05, 응용 01·02·03, 심화의 원리 과제와 특심화 공개 수치 테스트를 진행할 수 있습니다.
기본필수 04의 1 epoch 학습은 별도의 연결 점검이며 좋은 탐지 모델을 만드는 과정이라고 설명하지 않습니다.

## 데이터와 결과의 의미
- 기본필수: 24장 = train 12 / val 6 / test 6. 모든 그림에 정상 도형 3개.
- 응용·심화·특심화: 60장 = train 36 / val 12 / test 12. 정상 negative 이미지 포함.
- 준비 모델용 source: 별도 132장 = train 96 / val 24 / 보관 test 12. 목표 데이터·test는 source 학습에 넣지 않음.
- 클래스: `0=square`, `1=circle`, `2=triangle`. PPT 안전모 예시는 이 정상 도형 예제로 바꿨습니다.
- 영상: 160×128, 10 FPS, 30프레임. `track_ground_truth.csv`는 평가용 기하 정답이고 모델 입력이 아닙니다.
- Test는 구조·중복 확인 외에 모델 학습·추론·임계값 선택에 전달하지 않습니다. demo 영상은 개발 시연 자료입니다.

이미지·클래스·색의 관계가 쉬운 합성 데이터입니다. 실제 사람·도로·안전모 탐지 성능을 입증하지 않습니다.
GT에는 confidence가 없습니다. ground truth를 confidence=1.0인 모델 예측으로 취급하지 마세요.

## PPT와 구분해야 할 세 가지
1. **YOLO26 기본 추론은 end-to-end NMS-free입니다.** 고전 NMS 원리 과제는 별도 입력 후보로 수행합니다. YOLO26에서 `iou`만 바꾸면 반드시 NMS 결과가 바뀐다고 단정하지 않습니다.
2. 교육용 `AP101`은 지정한 101점 precision envelope 평균입니다. COCO의 crowd·ignore·area·maxDets를 모두 구현한 것이 아니며 Ultralytics 수치와 반드시 같지 않습니다.
3. 교육용 IoUTracker는 ByteTrack/BoT-SORT가 아닙니다. 순서·1:1 연결·stream 상태를 검증하는 원리 모델입니다. 실제 YOLO `.track()` 경로는 따로 있습니다.

## 실행과 제출
해당 단계의 README에 있는 순서로 진행합니다. 입력 경로는 코드 파일 위치 기준이므로 VS Code 실행 폴더가 달라도 작동하도록 구성했습니다.
기본필수 07~08은 `07_project.py`를 이어 사용합니다. 상위 단계는 각 프로젝트 README를 따릅니다.
최종 제출: 완성 코드, 생성된 표·영상, 자신의 해석, 실제 모델·데이터·설정·장치 기록. 네 단계 모두 제출하지 않습니다.
실제 YOLO 준비가 되지 않았다면 '실행 미완료'를 기록하세요. 원리 fixture의 결과로 실제 모델 과제를 통과 처리하지 않습니다.
