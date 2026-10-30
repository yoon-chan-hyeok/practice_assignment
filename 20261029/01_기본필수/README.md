# 기본필수 · Day9

**7개 Python 파일과 정상 CSV 1개만 사용합니다. 사용자 정의 함수·클래스·예외처리를 작성하지 않습니다.** 직접 완성할 부분은 B01~B09의 9곳입니다. 코드에 나오는 `nn.Linear` 등의 라이브러리 클래스는 제공된 사용법으로 호출합니다.

입력은 결측·중복·불량 값이 없는 작은 자료입니다. 처음부터 모든 파일을 한 번에 열지 말고, 아래 순서대로 한 파일씩 엽니다. 모든 경로는 코드 파일 위치 기준입니다.

```text
01_기본필수/
  README.md
  points.csv
  01_environment.py ... 07_project.py
```

환경 설치 안내는 상위 [README](../README.md)에 있습니다. 기본필수에서는 CPU만 사용합니다. `python 파일명.py` 명령은 이 폴더에서 실행합니다.

## GPU 동작 점검표

터미널에서 `nvidia-smi`를 직접 실행합니다. 명령을 찾지 못하는 경우도 그대로 기록합니다. 이 명령이 실행된 사실과 PyTorch CUDA 실행 성공은 별개입니다.

| 확인 항목 | 내 PC의 실제 결과 |
|---|---|
| Python 실행기 / 버전 | |
| PyTorch 버전 | |
| nvidia-smi 실행 여부 | |
| NVIDIA GPU 이름 / VRAM | |
| nvidia-smi의 드라이버 버전 | |
| nvidia-smi의 CUDA 지원 표시 | |
| torch.version.cuda(현재 PyTorch 빌드 정보) | |
| torch.cuda.is_available() | |
| 이번 실습의 실제 device | |
| 실제 Tensor 연산을 수행한 장치 | |

`is_available=False`만으로 GPU가 물리적으로 없다고 단정하지 않습니다. CPU 빌드·드라이버·가상환경·장치 노출을 구분합니다. CPU 진행은 허용되며 GPU 미보유를 감점하지 않습니다. NVIDIA가 없는 PC는 해당 항목에 '미해당/미확인'을 기입합니다.

## 실습 01 · 환경을 확인한다

**목표:** torch 버전·CUDA 빌드·사용 가능 여부를 구분하고 CPU Tensor 계산을 확인한다.

파일: `01_environment.py`

**B01** — 정상 숫자 1.0, 2.0을 담은 Tensor를 sample에 저장하세요. 아래 덧셈 결과가 [2.0, 3.0]이면 계산 환경이 준비된 것입니다.

```powershell
python 01_environment.py
```

**함수 읽기:** torch.tensor(data, dtype=...): 필수는 data. dtype/device/requires_grad는 선택입니다. CUDA 조회 함수는 괄호 안 인자가 없는 호출을 사용합니다.

**예상 출력(CPU 검수 예):**

```text
PyTorch: 2.10.0+cpu
PyTorch CUDA 빌드: None
CUDA 사용 가능: False
GPU: 이번 실행에서는 사용하지 않음
이 단계의 연산 장치: cpu
덧셈: [2.0, 3.0]
```

**완료 확인:** PPT의 nvidia-smi 결과를 위 점검표에 기록합니다. 기본필수는 GPU가 있어도 계산 장치를 CPU로 고정합니다. 실제 GPU 연산은 응용부터 진행합니다.

## 실습 02 · Tensor 모양을 읽는다

**목표:** 스칼라 (), 벡터 (3,), 행렬 (2,2)을 구분한다.

파일: `02_tensor.py`

**B02** — [[1.0, 2.0], [3.0, 4.0]]을 torch.float32의 2차원 Tensor matrix로 만드세요. 자료를 CPU로 옮기는 코드는 제공되어 있습니다.

```powershell
python 02_tensor.py
```

**함수 읽기:** Tensor.to(device): 이 예제는 장치를 명시합니다. 다른 호출 형태로 dtype만 바꿀 수도 있습니다. to()가 같은 조건이면 같은 Tensor를 반환할 수도 있습니다.

**예상 출력(CPU 검수 예):**

```text
스칼라: () torch.float32 cpu
벡터: (3,) torch.float32 cpu
행렬: (2, 2) torch.float32 cpu
행렬 값: [[1.0, 2.0], [3.0, 4.0]]
```

**완료 확인:** shape·dtype·device는 속성입니다. 괄호를 붙이지 않습니다. `.to("cpu")`의 반환값을 다시 변수에 저장합니다.

## 실습 03 · 자동 미분을 확인한다

**목표:** x=3에서 y=16, dy/dx=8을 손계산과 대조한다.

파일: `03_autograd.py`

**B03** — y = x² + 2x + 1을 Tensor 연산으로 작성하세요. x를 Python 숫자로 바꾸지 마세요. 계산 그래프가 이어져 있어야 합니다.

```powershell
python 03_autograd.py
```

**함수 읽기:** torch.tensor의 requires_grad는 선택 인자이며 기본 False. y.backward()는 스칼라 y에서 추가 필수 인자 없이 호출합니다. .item()은 원소가 하나인 Tensor를 Python 숫자로 꺼냅니다.

**예상 출력(CPU 검수 예):**

```text
y: 16.0
dy/dx: 8.0
```

**완료 확인:** backward가 y를 학습시키는 것이 아닙니다. x.grad에 미분값을 계산합니다.

## 실습 04 · ANN의 입력과 출력을 본다

**목표:** 2→8→2, 입력/출력 (4,2), 파라미터 42개를 확인한다.

파일: `04_ann.py`

**B04** — Sequential의 마지막 Linear를 수정해 출력 클래스 수가 2가 되게 하세요. 첫 Linear(2, 8)와 ReLU는 그대로 두세요. 모델 정의는 미리 제공했습니다.

```powershell
python 04_ann.py
```

**함수 읽기:** nn.Linear(in_features,out_features)는 두 인자가 필수. bias=True는 선택 기본값입니다. nn.ReLU()는 필수 인자가 없습니다. nn.Sequential은 연결할 층을 순서대로 받습니다.

**예상 출력(CPU 검수 예):**

```text
입력: (4, 2)
출력: (4, 2)
파라미터 수: 42
```

**완료 확인:** 4는 샘플 수, 마지막2는 특성 또는 클래스 수입니다. 확률을 아직 계산하지 않습니다.

## 실습 05 · 분류 손실을 계산한다

**목표:** logits (2,2)와 정답 (2,) long으로 CrossEntropyLoss를 계산한다.

파일: `05_loss.py`

**B05** — loss_fn에 logits와 target을 순서대로 넣어 loss를 계산하세요. logits에 softmax를 먼저 적용하지 마세요.

```powershell
python 05_loss.py
```

**함수 읽기:** nn.CrossEntropyLoss() 생성자는 인자 없이 사용 가능하며 reduction="mean"이 기본입니다. 생성한 loss_fn(logits,target) 호출에는 logits와 target이 필요합니다.

**예상 출력(CPU 검수 예):**

```text
logits: (2, 2)
target: (2,) torch.int64
loss: 0.126928
```

**완료 확인:** 정답 0·1은 각 행의 정답 클래스 번호입니다. softmax를 앞에 추가하지 않습니다.

## 실습 06 · 역전파와 갱신을 연결한다

**목표:** 순전파→손실→backward→step, 이전 gradient를 비우는 순서를 익힌다.

파일: `06_train.py`

**B06** — 현재 loss의 gradient를 계산하세요. 파라미터 값은 아직 바뀌지 않으며 .grad에 기울기가 들어갑니다.

**B07** — 현재 gradient를 사용해 파라미터를 한 번 갱신하세요. optimizer의 step 메서드를 호출합니다.

```powershell
python 06_train.py
```

**함수 읽기:** torch.optim.SGD(params,lr=0.1)는 params가 필수이고 lr을 이 수업에서 명시합니다. optimizer.zero_grad(), step()은 이 사용법에서 추가 인자가 필요 없습니다. model.train()/eval()과 torch.no_grad()의 역할은 서로 다릅니다.

**예상 출력(CPU 검수 예):**

```text
학습 전 loss: 0.473224
학습 후 loss: 0.106799
train 정확도: 1.0
주의: 위 정확도는 학습한 8건의 결과이며 새로운 자료의 성능이 아닙니다.
```

**완료 확인:** 여기서 출력하는 정확도는 학습한 8건의 train 정확도입니다. 최종 일반화 성능이라고 부르지 않습니다.

## 실습 07 · 결과 파일까지 만든다

**목표:** 20건 중 train12를 80회 학습하고 valid4로 확인한 뒤 세 결과를 저장한다.

파일: `07_project.py`

**B08** — 06번에서 배운 역전파와 파라미터 갱신 두 문장을 연결하세요. 이미 위에서 이전 gradient를 비우고 loss를 계산했습니다.

**B09** — 각 행에서 가장 큰 logit의 열 번호를 prediction으로 구하세요. argmax의 dim=1은 클래스 방향입니다. 결과 shape는 (4,)입니다.

```powershell
python 07_project.py
```

**함수 읽기:** logits.argmax(dim=1): dim은 선택 인자이지만 (N,2)의 클래스 축을 고르기 위해 1을 명시합니다. no_grad()는 평가 때 gradient 그래프 생성을 끕니다.

**예상 출력(CPU 검수 예):**

```text
분할: train 12 / valid 4 / test 4(보관)
train loss: 0.514554 -> 0.110675
valid 정확도: 1.0
valid 예측: [0, 0, 1, 1]
생성: gpu_check.txt, training_history.csv, final_metrics.json
```

**완료 확인:** 파일 읽기·쓰기와 모델 구조는 제공했습니다. B08·B09만 직접 완성합니다. test4는 보관합니다.

## 실습 08 · 같은 프로그램을 다시 실행하고 설명한다

`python 07_project.py`를 다시 실행합니다. 파일이 새로 생성/덮어쓰기 되는지 확인하고, 동일 환경의 이전 결과와 비교하세요. test를 평가하거나 모델 설정을 고르는 시간이 아닙니다.

| 파일 | 확인할 내용 |
|---|---|
| gpu_check.txt | 실제 PyTorch 환경과 selected_device=cpu |
| training_history.csv | epoch0(학습 전)부터80까지81행, 각 시점 train_loss_eval |
| final_metrics.json | train12·valid4, test_used=false, valid ID·정답·예측 |

### 내 설명 작성란

1. `.backward()`와 `.step()`은 각각 무엇을 바꾸나요? →
2. `zero_grad()`를 생략하면 어떤 일이 생기나요? →
3. `train 정확도`와 `valid 정확도`는 어떤 자료를 사용하나요? →
4. `eval()`만으로 gradient 기록이 꺼지나요? →
5. 정상 데이터 4건에서 정확도1.0이면 실제 서비스도 잘 동작한다고 할 수 있나요? →

**제출:** 완성한 코드, points.csv, 이 README의 설명, 생성된 세 결과 파일. Git 명령이나 별도 보고서 작성은 기본필수의 추가 구현 과제가 아닙니다.

### 막힐 때

`None`/`pass`/임시 숫자가 남아 있으면 TODO를 먼저 확인합니다. GPU가 없어도 CPU로 계속합니다. 04번 출력이(4,1)이면 마지막 Linear가 아직 미완성입니다. loss가 전혀 바뀌지 않으면 B06/B07 또는 B08의 backward·step을 확인합니다. 특성을 늘리거나 학습률을 바꾸기 전에 제공된 설정에서 실행 흐름부터 완성하세요.
