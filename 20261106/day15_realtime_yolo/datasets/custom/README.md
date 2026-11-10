# 선택 과제 · 새 데이터셋 준비

기본 웹캠 과제에는 이 폴더가 필요하지 않습니다. **추가 학습을 하는 학생만** 사용하세요. 이미지/라벨은 의도적으로 비어 있습니다. 실제 데이터를 자동 생성하거나 임의의 정답을 채우지 않습니다.

## 1. 데이터 배치

```text
custom/
├── data.yaml
├── images/
│   ├── train/  a001.jpg, a002.jpg, ...
│   ├── val/    b001.jpg, b002.jpg, ...
│   └── test/   c001.jpg, ...  # 선택·최종 평가용
└── labels/
    ├── train/  a001.txt, a002.txt, ...
    ├── val/    b001.txt, b002.txt, ...
    └── test/   c001.txt, ...
```

같은 split에서 이미지와 TXT의 stem이 같아야 합니다. `a001.jpg ↔ a001.txt`입니다. `valid`라는 폴더를 쓰는 데이터는 YAML의 키 **val**을 유지하고 값만 `images/valid`로 바꾸세요. 이름을 바꾸려면 images와 labels 아래 모두 일치시킵니다.

`train/images`, `train/labels` 형태를 유지하는 경우도 지원합니다. YAML에서 `train: train/images`, `val: valid/images`처럼 실제 경로를 씁니다. 이 스크립트는 각 split의 이미지 **폴더 한 개**를 지원하며 여러 경로 리스트나 image-list TXT는 지원하지 않습니다.

## 2. 클래스 정의

`data.yaml`의 `CHANGE_ME`를 실제 데이터셋의 클래스 ID 순서대로 바꿉니다.

```yaml
path: .
train: images/train
val: images/val
# test: images/test
names:
  0: my_object_a
  1: my_object_b
```

위 이름은 예시입니다. Kaggle 원본의 ID 0과 ID 1을 먼저 확인하고 실제 이름을 적으세요. 이전 도형 실습의 `square/circle/triangle`을 남겨 두거나 클래스 순서를 추측해서 쓰면 안 됩니다. 표시 안정성을 위해 짧은 영문 클래스명을 권장합니다.

프로젝트는 `path: .`를 **이 YAML이 있는 폴더**로 해석하고, 학습용 절대경로 YAML을 outputs에 생성합니다. 이 사용자 YAML을 프로젝트 스크립트가 아닌 Ultralytics CLI에 직접 전달하면 상대경로 해석이 달라질 수 있으므로, CLI에는 생성된 `dataset_active.yaml`을 사용하세요.

## 3. YOLO TXT 라벨

한 줄에 한 객체를 기록합니다. 픽셀 좌표가 아니라 이미지 크기로 정규화한 값입니다. [공식 데이터 형식: README 출처 3]

```text
# 실제 라벨 파일에는 설명 주석을 넣지 않습니다. 아래 한 줄만 예시입니다.
0 0.500000 0.500000 0.200000 0.300000
```

형식은 `class_id center_x center_y width height`입니다. 클래스 ID는 0부터, 중심은 0~1, 너비/높이는 0 초과~1이며 박스는 이미지 안에 있어야 합니다. 이미지가 아니라 바운딩박스의 클래스 라벨입니다. 분류 폴더 데이터만으로는 이 객체 탐지 학습을 할 수 없습니다.

공식 로더는 객체 없는 이미지의 라벨 누락을 허용할 수 있지만, **이 프로젝트의 점검기는 의도적 배경과 라벨 누락을 구분하려고 빈 TXT를 요구**합니다. 박스를 모른다는 이유로 빈 TXT를 만들면 실제 객체가 배경으로 학습되므로 금지합니다.

## 4. 분할·누수 주의

같은 원본 이미지의 복사/증강본, 같은 촬영 장면의 연속 프레임을 train/val/test에 나누어 넣지 않습니다. 촬영 세션이나 원본 단위로 분리하고 출처/분할 기준을 기록하세요. `check_dataset.py`는 **파일 바이트 동일 중복**만 검사하므로 시각적으로 유사한 데이터 누수는 별도 확인해야 합니다.

클래스별 학습·검증 표본이 있어야 비교를 해석할 수 있습니다. 시간 안에 새로운 수집/라벨링/충분한 학습까지 모두 끝내려 하지 말고, 이미 라벨이 준비된 소규모 데이터를 사용하세요. 정해진 이미지 수만 충족한다고 일반화 성능이 보장되는 것은 아닙니다.

## 5. 실행

프로젝트 최상위 폴더에서 실행합니다.

```powershell
# 1) 경로/클래스/라벨/좌표 및 train-val 파일 중복 점검
python check_dataset.py

# 2) 기존 사전학습 가중치에서 새 학습 실행. 아래 2 epoch는 실행 확인용
python train_custom.py --epochs 2 --imgsz 320 --batch 4

# 3) 최신 추가 학습 모델을 같은 val에 정량 평가
python evaluate_custom.py

# 4) 카메라에 적용
python main.py --model custom
```

학습 시간은 `outputs/train_.../training_summary.json`, 검증 결과는 `outputs/eval_.../metrics.json`과 `class_metrics.csv`에 저장됩니다. 모델 생성/초기 다운로드 시간은 학습 호출 시간에 포함하지 않습니다. Val 평가의 candidate confidence는 0.001이며 웹캠 표시 기준 0.25와 다릅니다. 단일 threshold의 화면 캡처 수치와 mAP를 동일한 측정이라고 쓰지 않습니다.

파일 경로를 직접 지정할 수도 있습니다.

```powershell
python evaluate_custom.py --model "outputs/train_실제폴더명/weights/best.pt" --data datasets/custom/data.yaml
python main.py --model "outputs/train_실제폴더명/weights/best.pt"
```

`train_실제폴더명`은 실제 출력 폴더명으로 바꿉니다. `--model custom`은 가장 최근 **성공한** 학습의 best.pt를 사용하므로 이전 실험을 비교하려면 파일 경로를 직접 지정합니다.

## 6. 최종 Test는 선택

실험 조건을 고정하고 최종 결과를 확인할 때만 YAML에 `test: images/test`를 추가한 후 아래를 실행합니다.

```powershell
python evaluate_custom.py --data datasets/custom/data.yaml --split test
```

보고서에는 val/test를 구분합니다. 기본 수업, 학습, 자동 점검은 Test를 읽지 않습니다. Test 결과를 보고 반복적으로 설정을 바꾸면 독립적인 최종 평가로 해석할 수 없습니다.

## 7. 미완료 처리

학습이 끝나지 않았으면 보고서 선택 섹션에 **“준비/시도/미완료”**를 기록합니다. 예측 점수나 mAP를 가정해 채우지 않습니다. 기본 웹캠 과제와 보고서를 완성하면 필수 수행은 충족합니다.
