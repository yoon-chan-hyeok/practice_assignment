# 응용 · 변환·평가·전이학습·계측을 연결하기

코드는 이 폴더에 그대로 두고 입력 `data/`, 직접 생성하는 결과 `outputs/`만 구분합니다. 함수·클래스를 새로 정의할 필요 없이 TODO 10곳을 완성합니다. 데이터는 RGB PNG 100장(train60/valid20/test20)입니다.

01~05·07·08은 오프라인 CPU로 실행할 수 있습니다. 06의 실제 가중치만 사전 준비가 필요합니다. 08은 CNN 프로젝트를 독립적으로 완성합니다. 06 결과를 추가 비교할 때는 `transfer_comparison.csv`의 입력 크기·epoch·lr 차이를 반드시 설명하세요.

## 오늘 처음 만나는 API의 읽는 법

| 호출 | 하는 일 | 필수 인자 | 주요 선택 인자·기본값 |
|---|---|---|---|
| `torch.rand(4,3,32,32)` | 해당 모양의 난수 Tensor | 모양을 정하는 크기 | `dtype`, `device`; 여기서는 float32·CPU |
| `x.permute(1,2,0)` | 값은 그대로, 축 순서 변경 | 모든 축의 새 순서 | 추가 선택 인자 없음 |
| `x.unsqueeze(0)` | 크기 1의 축 추가 | `dim` | 추가 선택 인자 없음 |
| `nn.Conv2d(3,8,3,padding=1)` | 학습 가능한 필터로 특징 계산 | `in_channels, out_channels, kernel_size` | `stride=1, padding=0, dilation=1, groups=1, bias=True` |
| `nn.MaxPool2d(2)` | 작은 영역의 최댓값 선택 | `kernel_size` | `stride=None`이면 커널 크기 사용, `padding=0` |
| `nn.AdaptiveAvgPool2d(1)` | 채널별 목표 공간 크기로 평균 | `output_size` | 이 예제의 추가 선택 인자 없음 |
| `nn.Flatten()` | 공간 축을 긴 벡터로 합침 | 없음 | `start_dim=1, end_dim=-1` |
| `nn.Linear(32,2)` | 특성 32개를 클래스 점수 2개로 변환 | `in_features, out_features` | `bias=True` |
| `ImageFolder(root, transform=...)` | 클래스 폴더에서 이미지·라벨 읽기 | `root` | `transform=None`, `target_transform=None` |
| `Compose([...])` | 여러 변환을 차례대로 적용 | 변환 목록 | 없음 |
| `Resize((32,32))` | 입력 크기 변경 | `size` | `interpolation`, `antialias` 등 |
| `ToTensor()` | PIL 이미지→CHW float Tensor | 없음 | 없음; 이 PNG의 값은 보통 0~1 |
| `Normalize(mean,std)` | 채널별 `(x-mean)/std` | `mean`, `std` | `inplace=False` |
| `DataLoader(dataset, batch_size=4)` | 이미지들을 배치로 묶음 | `dataset` | `batch_size=1, shuffle=False, num_workers=0, drop_last=False` |
| `resnet18(weights=...)` | ResNet18 모듈 생성 | 필수 사용자 인자 없음 | `weights=None, progress=True`; 여기서는 실제 가중치를 명시 |
| `weights.transforms()` | 해당 사전학습 가중치의 변환 생성 | 필수 사용자 인자 없음 | 기본 Resize·Crop·Normalize 사용 |

층을 만드는 호출과 데이터를 넣는 호출은 다릅니다. `conv=nn.Conv2d(...)`로 층을 만들고 `y=conv(x)`로 계산합니다. `CrossEntropyLoss`에는 Softmax 이전 logits와 long 정수 라벨을 넣습니다.


## 실습 06 시작 전: 실제 사전학습 가중치 준비

`resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)`는 공식 ImageNet 사전학습 가중치를 사용합니다. 최초 약 45MB 다운로드와 다음 실행을 위한 캐시가 필요합니다. 수업 전에 교사가 준비하세요.

```powershell
python -c "from torchvision.models import resnet18, ResNet18_Weights; resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)"
python -c "import torch; print(torch.hub.get_dir())"
```

오프라인 PC에는 **공식 사이트에서 받은** `resnet18-f37072fd.pth`를 출력된 hub 폴더의 `checkpoints` 안에 복사합니다. 가중치 파일은 이 ZIP에 넣지 않았습니다. 교사용 `운영/prepare_weights.py`로 다운로드·해시·전처리를 점검할 수 있습니다.

**이번 제작 환경에서는 공식 가중치 다운로드가 차단되어 실제 사전학습 모델의 학습·성능을 실행 검증하지 못했습니다.** 전이학습 파일에 임의의 정확도를 예상값으로 넣지 않았습니다. 무작위 가중치로 수행한 테스트는 동결·파라미터 그룹·BN 상태의 구조 검사일 뿐 전이학습 성능 검증이 아닙니다.

`weights=None`으로 바꿔 실행한 결과를 전이학습 결과로 제출하지 않습니다. 가중치를 준비하지 못했다면 해당 실습은 **미실행**으로 기록하고 교사 시연으로 동결 범위·파라미터 수를 확인합니다. 다른 실습은 독립적으로 진행할 수 있습니다.

## 01_axes.py · 축 변환과 표시

PPT 12쪽과 연결합니다. 이 단계 폴더를 터미널의 현재 위치로 둡니다.

```powershell
python 01_axes.py
```

### 직접 완성할 부분

- **A01**: 채널 축을 마지막으로 보내 HWC를 만든다. 힌트: permute(1, 2, 0)

### 확인할 결과

```text
CHW / HWC / NCHW: (3, 64, 64) (64, 64, 3) (1, 3, 64, 64)
왕복 값 일치: True
```

**완료·설명**: N/C/H/W를 자기 말로 설명하고 같은 값을 다른 축 순서로 표시한 것과 이미지 내용이 변한 것을 구분합니다.

## 02_stride.py · Stride 비교

PPT 22쪽과 연결합니다. 이 단계 폴더를 터미널의 현재 위치로 둡니다.

```powershell
python 02_stride.py
```

### 직접 완성할 부분

- **A02**: 현재 반복의 stride를 Conv2d에 전달한다. 힌트: stride=stride

### 확인할 결과

```text
stride          shape  params   macs
      1 (4, 8, 32, 32)     224 884736
      2 (4, 8, 16, 16)     224 221184
```

**완료·설명**: 입력·출력의 공간 크기와 학습 파라미터 수를 계산하고, stride가 바뀌어도 파라미터 수가 그대로일 수 있는 이유를 설명합니다.

## 03_downsample.py · Pooling과 stride Conv

PPT 34쪽과 연결합니다. 이 단계 폴더를 터미널의 현재 위치로 둡니다.

```powershell
python 03_downsample.py
```

### 직접 완성할 부분

- **A03**: 각 downsampling 층을 입력 x에 적용한다. 힌트: layer(x)

### 확인할 결과

```text
method          shape  params
        pool (4, 8, 16, 16)       0
conv_stride2 (4, 8, 16, 16)     584
```

**완료·설명**: Conv/Pool/Adaptive Pool/Flatten/Head를 거치는 shape를 적고, 마지막 출력 2개가 클래스 점수라는 것을 설명합니다.

## 04_transforms.py · train/valid 변환 분리

PPT 47쪽과 연결합니다. 이 단계 폴더를 터미널의 현재 위치로 둡니다.

```powershell
python 04_transforms.py
```

### 직접 완성할 부분

- **A04**: valid에는 Resize와 ToTensor만 적용한다. 힌트: 평가에는 무작위 회전·반전을 넣지 않는다.

### 확인할 결과

```text
valid 동일: True
shape: (3, 64, 64)
train 3개 동일 여부: False
```

**완료·설명**: `class_to_idx`에서 0·1의 의미를 확인합니다. train과 valid가 같은 클래스 순서를 사용하고, valid에서 무작위 변환이 없는 이유를 설명합니다.

## 05_evaluate.py · Best 복원·오류 분석

PPT 58쪽과 연결합니다. 이 단계 폴더를 터미널의 현재 위치로 둡니다.

```powershell
python 05_evaluate.py
```

### 직접 완성할 부분

- **A05**: loss 역전파와 가중치 갱신을 순서대로 실행한다. 힌트: loss.backward() → optimizer.step()

### 확인할 결과

```text
epoch  train_loss  train_accuracy  valid_loss  valid_accuracy
     1      0.6187          0.9167      0.6195            0.95
     2      0.6333          0.5000      0.6283            0.50
     3      0.3657          0.9833      0.3722            0.95
     4      0.1528          1.0000      0.1548            1.00
     5      0.0505          1.0000      0.0553            1.00
best epoch: 5
혼동행렬 행=실제, 열=예측:
 [[10, 0], [0, 10]]
클래스별 정답 수: [10, 10] / [10, 10]
```

**완료·설명**: valid loss가 최소인 epoch를 찾고 마지막 모델과 best 모델의 차이를 설명합니다. 정답이 높아도 간단한 합성 이미지의 소표본 결과임을 함께 적습니다.

## 06_transfer.py · Head와 layer4 비교

PPT 70쪽과 연결합니다. 이 단계 폴더를 터미널의 현재 위치로 둡니다.

```powershell
python 06_transfer.py
```

실제 사전학습 가중치가 필요합니다. 위 사전 준비를 먼저 확인합니다. 제작 환경의 실제 전이학습 실행 결과는 **미검증**입니다. 파라미터 수 1026(Head-only)과 입력 `[B,3,224,224]`를 먼저 확인하고 정확도는 본인 환경에서 기록합니다.

### 직접 완성할 부분

- **A06**: partial일 때만 layer4의 미분을 켠다. 힌트: requires_grad=True. BN eval은 유지한다.

### 확인할 결과


**완료·설명**: `requires_grad=False`가 BN의 running 통계를 자동 고정하지 않는 이유를 설명합니다. `eval()`은 gradient 계산 자체를 끄지 않으므로 fc는 학습할 수 있습니다.

## 07_benchmark.py · CPU/GPU 측정

PPT 81쪽과 연결합니다. 이 단계 폴더를 터미널의 현재 위치로 둡니다.

```powershell
python 07_benchmark.py
```

### 직접 완성할 부분

- **A07**: GPU 작업 완료를 기다린 후 종료 시간을 읽는다. 힌트: CUDA인 경우 torch.cuda.synchronize(device)

### 확인할 결과

`seconds > 0`, `images_per_second = images / seconds`입니다. CPU VRAM은 빈 값/N/A입니다. 정상 이미지가 한 epoch에 한 번씩 처리되는지 확인합니다. CPU-only 환경에서 GPU 결과를 0으로 채우지 않습니다. 실제 시간은 예상 숫자가 아닙니다.

**완료·설명**: 데이터 로딩 포함 여부·이미지 크기·배치·워밍업·장치·반복 수를 기록합니다. 서로 다른 측정 범위의 속도를 직접 비교하지 않습니다.

## 08_project.py · 이미지 분류 결과표

PPT 87쪽과 연결합니다. 이 단계 폴더를 터미널의 현재 위치로 둡니다.

```powershell
python 08_project.py
```

### 직접 완성할 부분

- **A08**: 학습 갱신을 연결합니다. `backward → step` 순서를 지킵니다.
- **A09**: 혼동행렬과 클래스별 support·정답 수·Precision·Recall·F1을 계산합니다. 0분모는 0.0입니다. 행=실제, 열=예측입니다.
- **A10**: valid의 실제 오답만 원본 순서대로 `error_samples.csv`에 저장합니다. 파일 상대경로·실제 라벨·예측 라벨·예측 confidence를 포함합니다. 오답 0개이면 헤더만 있는 CSV가 정답이며 라벨을 바꾸지 않습니다.

### 확인할 결과

```text
epoch  train_loss  train_accuracy  valid_loss  valid_accuracy
     1      0.6187          0.9167      0.6195            0.95
     2      0.6333          0.5000      0.6283            0.50
     3      0.3657          0.9833      0.3722            0.95
     4      0.1528          1.0000      0.1548            1.00
     5      0.0505          1.0000      0.0553            1.00
best epoch: 5
혼동행렬 행=실제, 열=예측:
 [[10, 0], [0, 10]]
클래스별 정답 수: [10, 10] / [10, 10]
CNN 결과 저장 완료. 06_transfer의 표는 입력 크기·학습량 차이를 함께 비교한다.
```

**완료·설명**: `history`, `model_comparison`, 예측표와 best 가중치가 생성되는지 확인하고 3문장으로 결과와 한계를 설명합니다. **test는 보관합니다.**

## 비교 기록

| 모델 | 입력 크기 | 학습 범위 | epoch | valid loss/정확도 | 시간 범위·장치 | 한계 |
|---|---:|---|---:|---|---|---|
| SmallCNN | 32 | 전체 | 5 | 직접 기록 | 직접 기록 | 합성·소표본 |
| ResNet18 Head | 224 | fc | 1 | 직접 기록/미실행 | 직접 기록/미측정 | 비교 조건 차이 |
| ResNet18 Partial | 224 | layer4+fc, BN 통계 고정 | 1 | 직접 기록/미실행 | 직접 기록/미측정 | 짧은 학습 |

오류 이미지의 경로는 `cnn_predictions.csv`의 actual과 predicted가 다른 행에서 확인합니다. 클래스를 찾는 순서는 정답 수뿐 아니라 전체 클래스 수와 함께 확인합니다. `learning_curve.png`는 08이 실제 생성합니다.

## v2 추가 산출물과 완료 기준
`08_project.py`가 `outputs/class_metrics.csv`(두 클래스)와 `outputs/error_samples.csv`(실제 오답만)를 추가 생성합니다. 출력이 0행이어도 데이터 손실/실패가 아닐 수 있습니다. `confusion_matrix.csv`와 support 합계 20이 맞는지 확인하세요. CPU 정답에서는 5 epoch 후 오답 0건입니다. 이는 합성 줄무늬 자료의 결과이지 자연 사진 성능의 보증이 아닙니다.

설명 질문: 전체 정확도가 높아도 클래스별 Recall을 확인해야 하는 이유는 무엇인가? confidence가 높은 오답이 있다면 어떤 입력과 학습 조건부터 검토할 것인가?

## 최신 수정판 08번 실제 출력

아래는 A09·A10을 모두 구현한 CPU 참조 출력입니다. 기존 08번 설명에 클래스별 지표·오답 파일이 추가됩니다.

```text
클래스별 지표 행 수: 2 실제 오답 수: 0
 epoch  train_loss  train_accuracy  valid_loss  valid_accuracy
     1      0.6187          0.9167      0.6195            0.95
     2      0.6333          0.5000      0.6283            0.50
     3      0.3657          0.9833      0.3722            0.95
     4      0.1528          1.0000      0.1548            1.00
     5      0.0505          1.0000      0.0553            1.00
best epoch: 5
혼동행렬 행=실제, 열=예측:
 [[10, 0], [0, 10]]
클래스별 정답 수: [10, 10] / [10, 10]
CNN 결과 저장 완료. 06_transfer의 표는 입력 크기·학습량 차이를 함께 비교한다.
```
