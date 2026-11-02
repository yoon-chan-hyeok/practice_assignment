# 기본필수 · CNN을 짧은 코드로 확인하기

이 폴더에는 실습용 Python 8개와 README, ImageFolder에 필요한 `data/`만 있습니다. 사용자 정의 함수·클래스·예외처리는 만들지 않습니다. 생성되는 CSV·PT도 이 폴더에 저장합니다.

```text
01_기본필수/
  README.md
  01_tensor.py ... 08_project.py
  data/
    train/horizontal/  train/vertical/
    valid/horizontal/  valid/vertical/
    test/horizontal/   test/vertical/  ← 보관, 실행에 사용하지 않음
```

PPT의 `SmallCNN` 클래스 대신 같은 Conv16→Conv32→Global Pool→Head를 `nn.Sequential`로 제공합니다. 이번 자료는 두 클래스이므로 Head 출력은 2개입니다. 기본 학습 입력은 32×32, 5 epoch, CPU·정상 이미지입니다. 코드의 읽기·모델 생성·결과 저장은 제공되며 TODO 9곳만 직접 완성합니다.

한꺼번에 모든 파일을 읽지 말고 01→02→03→04→05→06→07→08 순서로 진행합니다. 01~07은 서로의 출력 파일에 의존하지 않습니다. 06은 사전학습 가중치가 준비된 경우만 실행하며 다른 파일을 막지 않습니다.

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

## 01_tensor.py · 이미지 Tensor

PPT 12쪽과 연결합니다. 이 단계 폴더를 터미널의 현재 위치로 둡니다.

```powershell
python 01_tensor.py
```

### 직접 완성할 부분

- **B01**: RGB 이미지 4장, 높이·너비 32인 Tensor를 만든다. 힌트: 첫 크기를 4로 수정한다.

### 확인할 결과

```text
shape: (4, 3, 32, 32)
dtype: torch.float32
device: cpu
첫 이미지: (3, 32, 32)
```

**완료·설명**: N/C/H/W를 자기 말로 설명하고 같은 값을 다른 축 순서로 표시한 것과 이미지 내용이 변한 것을 구분합니다.

## 02_conv.py · 합성곱

PPT 22쪽과 연결합니다. 이 단계 폴더를 터미널의 현재 위치로 둡니다.

```powershell
python 02_conv.py
```

### 직접 완성할 부분

- **B02**: 3입력·8출력·3×3·padding 1의 합성곱 층을 만든다. 힌트: 선택 인자 padding=1을 추가한다.

### 확인할 결과

```text
입력: (4, 3, 32, 32)
출력: (4, 8, 32, 32)
파라미터: 224
```

**완료·설명**: 입력·출력의 공간 크기와 학습 파라미터 수를 계산하고, stride가 바뀌어도 파라미터 수가 그대로일 수 있는 이유를 설명합니다.

## 03_pool.py · Pooling과 CNN

PPT 34쪽과 연결합니다. 이 단계 폴더를 터미널의 현재 위치로 둡니다.

```powershell
python 03_pool.py
```

### 직접 완성할 부분

- **B03**: 출력 높이·너비를 절반으로 만드는 MaxPool을 작성한다. 힌트: 커널 크기를 2로 바꾼다.

### 확인할 결과

```text
Conv2d (4, 16, 32, 32)
ReLU (4, 16, 32, 32)
MaxPool2d (4, 16, 16, 16)
Conv2d (4, 32, 16, 16)
ReLU (4, 32, 16, 16)
MaxPool2d (4, 32, 8, 8)
AdaptiveAvgPool2d (4, 32, 1, 1)
Flatten (4, 32)
Linear (4, 2)
```

**완료·설명**: Conv/Pool/Adaptive Pool/Flatten/Head를 거치는 shape를 적고, 마지막 출력 2개가 클래스 점수라는 것을 설명합니다.

## 04_images.py · 이미지 읽기

PPT 47쪽과 연결합니다. 이 단계 폴더를 터미널의 현재 위치로 둡니다.

```powershell
python 04_images.py
```

### 직접 완성할 부분

- **B04**: data/train을 주어진 transform으로 읽는다. 힌트: transform=transform을 전달해야 Tensor 배치를 만들 수 있다.

### 확인할 결과

```text
학습 이미지: 12
클래스: {'horizontal': 0, 'vertical': 1}
배치: (4, 3, 32, 32) (4,)
라벨: [0, 0, 0, 0]
```

**완료·설명**: `class_to_idx`에서 0·1의 의미를 확인합니다. train과 valid가 같은 클래스 순서를 사용하고, valid에서 무작위 변환이 없는 이유를 설명합니다.

## 05_train.py · CNN 학습과 Best

PPT 58쪽과 연결합니다. 이 단계 폴더를 터미널의 현재 위치로 둡니다.

```powershell
python 05_train.py
```

### 직접 완성할 부분

- **B05**: loss를 역전파하고 optimizer로 한 번 갱신한다. 힌트: loss.backward() 다음 optimizer.step().

### 확인할 결과

```text
epoch=1 train_loss=0.6703 valid_loss=0.6718 valid_acc=0.50
epoch=2 train_loss=0.6389 valid_loss=0.6442 valid_acc=0.50
epoch=3 train_loss=0.5896 valid_loss=0.6020 valid_acc=1.00
epoch=4 train_loss=0.5209 valid_loss=0.5423 valid_acc=1.00
epoch=5 train_loss=0.4358 valid_loss=0.4664 valid_acc=1.00
선택한 epoch: 5
```

**완료·설명**: valid loss가 최소인 epoch를 찾고 마지막 모델과 best 모델의 차이를 설명합니다. 정답이 높아도 간단한 합성 이미지의 소표본 결과임을 함께 적습니다.

## 06_transfer.py · 실제 전이학습

PPT 70쪽과 연결합니다. 이 단계 폴더를 터미널의 현재 위치로 둡니다.

```powershell
python 06_transfer.py
```

실제 사전학습 가중치가 필요합니다. 위 사전 준비를 먼저 확인합니다. 제작 환경의 실제 전이학습 실행 결과는 **미검증**입니다. 파라미터 수 1026(Head-only)과 입력 `[B,3,224,224]`를 먼저 확인하고 정확도는 본인 환경에서 기록합니다.

### 직접 완성할 부분

- **B06**: 기존 parameter의 requires_grad를 False로 설정한다. 힌트: 새 fc를 만들기 전에 Backbone의 미분을 끈다.

### 확인할 결과


**완료·설명**: `requires_grad=False`가 BN의 running 통계를 자동 고정하지 않는 이유를 설명합니다. `eval()`은 gradient 계산 자체를 끄지 않으므로 fc는 학습할 수 있습니다.

## 07_benchmark.py · CPU 시간 측정

PPT 81쪽과 연결합니다. 이 단계 폴더를 터미널의 현재 위치로 둡니다.

```powershell
python 07_benchmark.py
```

### 직접 완성할 부분

- **B07**: 처리한 이미지 수를 경과 초로 나눠 images/s를 구한다. 힌트: seen / seconds

### 확인할 결과

`seconds > 0`, `images_per_second = images / seconds`입니다. CPU VRAM은 빈 값/N/A입니다. 정상 이미지가 한 epoch에 한 번씩 처리되는지 확인합니다. CPU-only 환경에서 GPU 결과를 0으로 채우지 않습니다. 실제 시간은 예상 숫자가 아닙니다.

**완료·설명**: 데이터 로딩 포함 여부·이미지 크기·배치·워밍업·장치·반복 수를 기록합니다. 서로 다른 측정 범위의 속도를 직접 비교하지 않습니다.

## 08_project.py · CNN 종합 프로젝트

PPT 87쪽과 연결합니다. 이 단계 폴더를 터미널의 현재 위치로 둡니다.

```powershell
python 08_project.py
```

### 직접 완성할 부분

- **B08**: model 순전파 후 정답과 CrossEntropyLoss를 계산한다. 힌트: loss_fn(logits, y_train)
- **B09**: 역전파 후 가중치를 갱신한다. 힌트: loss.backward(); optimizer.step()

### 확인할 결과

```text
epoch  train_loss  valid_loss  train_accuracy  valid_accuracy
     1      0.6703      0.6718             0.5             0.5
     2      0.6389      0.6442             0.5             0.5
     3      0.5896      0.6020             1.0             1.0
     4      0.5209      0.5423             1.0             1.0
     5      0.4358      0.4664             1.0             1.0
best epoch: 5 valid accuracy: 1.0
저장: history.csv, model_comparison.csv, valid_predictions.csv, best_model.pt
test 4장은 읽거나 모델에 전달하지 않았다.
```

**완료·설명**: `history`, `model_comparison`, 예측표와 best 가중치가 생성되는지 확인하고 3문장으로 결과와 한계를 설명합니다. **test는 보관합니다.**

## 마지막 기록(이 README에 직접 작성)

1. 오늘 학습한 입력/출력 shape: ______
2. 내 best epoch와 그때 valid loss·정확도: ______
3. SmallCNN과 ResNet18의 입력 크기·학습 범위 차이: ______
4. CPU 측정 범위와 GPU 미측정 여부: ______
5. 이 자료의 한계: 합성 이미지/표본 수/실제 사진과의 차이 ______

작은 정상 이미지에서 높은 정확도를 얻었더라도 실제 서비스 성능은 아닙니다. 구현과 설명을 평가하며 점수 자체를 높이려고 test를 보지 않습니다.
