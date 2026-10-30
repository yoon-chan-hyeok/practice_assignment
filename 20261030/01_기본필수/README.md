# Day10 · 기본필수

**이 폴더를 VS Code로 열고 아래 01번부터 진행합니다. README 하나에서 실습 01~08을 모두 안내합니다.**

Python 7개·CSV 1개·이 README만 있습니다. 처음에는 하위 폴더나 모델 저장 파일이 없습니다. 실행 후 결과 CSV/PNG는 같은 폴더에 생성됩니다.
모든 모델은 CPU로 실행합니다. 함수·클래스 정의·예외처리·자동 테스트 작성은 없습니다.

## 준비와 실행
전날 PyTorch가 정상 실행된 가상환경을 그대로 사용합니다. 오늘은 재설치·CUDA 변경이 과제가 아닙니다.

1. ZIP을 새 폴더에 압축 해제합니다. 이전 자료에 덮어쓰지 않습니다.
2. VS Code에서 **자신의 난이도 폴더**를 열고, 전날 사용한 Python 인터프리터를 선택합니다.
3. 새 터미널에서 `python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"`로 확인합니다.
4. PyTorch가 이미 있으면 `python -m pip install pandas matplotlib`만 필요합니다. 기본 데이터 처리는 pandas, 그림은 Matplotlib입니다.
5. PyTorch가 없다면 강사와 [공식 설치 선택기](https://docs.pytorch.org/get-started/locally/)에서 OS/CPU/CUDA에 맞는 명령을 정합니다. 모든 코드는 CPU로 수행 가능합니다. `torchvision`은 오늘 사용하지 않습니다.

실제 검수: Python 3.13.5 / PyTorch 2.10.0+cpu / NumPy 2.3.5 / pandas 2.2.3 / Matplotlib 3.10.8 / Linux.
PPT에 적힌 PyTorch 2.14·CUDA 13 조합을 이 환경에서 검증한 것은 아닙니다. Windows·macOS·실제 NVIDIA GPU 실행은 미검증입니다.
PPT API 설명과 검수 환경의 버전을 구분하고, 정상인 GPU 환경을 CPU 패키지로 덮어쓰지 마세요.

모든 실행 명령은 해당 `.py`가 있는 폴더의 터미널 기준입니다. Windows는 `cd "경로"`, macOS/Linux도 `cd "경로"`를 사용할 수 있습니다.
`python` 명령이 없을 때는 기관 PC 설정에 따라 `py`(Windows) 또는 `python3`를 사용합니다.
파일은 `__file__` 위치를 기준으로 읽으므로 다른 작업 폴더에서도 절대 경로 실행이 가능합니다.

## 오늘의 공통 실험 규칙
- **test는 오늘도 보관합니다.** 모형 선택·Early Stopping·학습률 조정에는 train/valid만 사용합니다.
- 후보마다 모델·Optimizer를 새로 만들고 seed를 재설정합니다. 앞 후보의 학습을 이어받지 않습니다.
- mini-batch 비교에서는 shuffle Generator도 같은 seed로 새로 만듭니다. 데이터 순서는 Dropout의 난수와 분리합니다.
- `train_loss_step`은 학습 도중 각 배치에서 측정한 손실입니다. 곡선의 `train_loss_eval`과 `valid_loss`는 **epoch 종료 후 같은 모델을 eval 모드로** 측정합니다.
- 후보·seed·epoch·batch size를 사전에 기록하고, 좋지 않은 결과도 그대로 남깁니다. ‘개선 후보’가 반드시 개선되어야 하는 과제가 아닙니다.
- 같은 epoch 수가 같은 optimizer 갱신 횟수는 아닙니다. 배치 실험에서는 iterations/total_steps도 확인합니다.
- 반복 seed 편차는 이 작은 실험의 변동입니다. 일반적인 알고리즘 순위나 통계적 유의성을 주장하지 않습니다.
- 모든 수치는 작은 합성 자료의 교육용 결과입니다. 실서비스 성능·GPU 속도 우위를 의미하지 않습니다.

## 새 함수·클래스 빠른 사전
‘선택값’ 열은 **이 실습에서 명시하는 값**이며, 라이브러리의 모든 기본값 목록은 아닙니다.

| 호출 | 역할·반환 | 필수 인자 | 이번에 다룰 선택 인자 |
|---|---|---|---|
| `torch.optim.SGD(params, ...)` | gradient로 파라미터를 갱신할 Optimizer 생성 | `params`: 보통 `model.parameters()` | `lr`, `momentum`, `weight_decay` |
| `torch.optim.AdamW(params, ...)` | 적응적 갱신과 분리된 가중치 감쇠 | `params` | `lr`, `weight_decay`; 기본 decay는 0.01이므로 비교 실험에서 0을 명시 |
| `optimizer.zero_grad()` | 이전 gradient를 비움 | 없음 | `set_to_none=True`: gradient를 None으로 초기화 |
| `optimizer.step()` | 현재 `.grad`로 한 번 갱신 | 없음 | 일반 학습에서는 선택 `closure`를 사용하지 않음 |
| `TensorDataset(*tensors)` | 같은 첫 차원의 Tensor를 묶은 Dataset | 이 실습에서는 X, y 두 Tensor | 추가 Tensor를 넣으면 함께 배치화됨 |
| `DataLoader(dataset, ...)` | Dataset을 배치로 순회하는 객체 | `dataset` | `batch_size`, `shuffle`, `generator`, `num_workers=0`, `drop_last=False` |
| `nn.Dropout(p=0.5)` | train에서 일부 activation을 0으로, eval에서 그대로 전달 | 없음 | `p`: 제거 확률, `inplace=False` |
| `nn.BatchNorm1d(num_features, ...)` | 특성별 batch 통계와 running 통계 사용 | `num_features`: 앞 Linear 출력 열 수 | `momentum=0.1`, `eps=1e-5`, `affine=True`, `track_running_stats=True` |
| `model.train(mode=True)` | 모듈 모드 설정, self 반환 | 없음 | `mode`; `eval()`은 `train(False)`에 해당 |
| `torch.no_grad()` | 안쪽 계산의 gradient 기록을 끄는 문맥 | 없음 | 모드를 바꾸지는 않음 |
| `ReduceLROnPlateau(optimizer, ...)` | valid 지표가 개선되지 않을 때 lr 감소 | `optimizer` | `mode='min'`, `factor`, `patience`, `threshold`, `threshold_mode` |
| `scheduler.step(valid_loss)` | Plateau의 상태·lr 갱신 | Plateau는 `metrics` | 기본적으로 epoch 번호는 직접 전달하지 않음 |
| `CosineAnnealingLR(optimizer, T_max, ...)` | 미리 정한 cosine 일정으로 lr 변경 | `optimizer`, `T_max` | `eta_min`; `.step()`에 loss를 넣지 않음 |
| `copy.deepcopy(model.state_dict())` | best 시점 가중치·BN 버퍼의 독립 사본 | 복사할 객체 | 단순 대입으로 대체하면 값이 따라 바뀔 수 있음 |
| `torch.save(obj, path)` | 직접 만든 상태 저장 | `obj`, 저장 경로 | 전체 Module 대신 state_dict 사용 |
| `torch.load(path, ...)` | 직접 저장한 파일 읽기 | 파일 경로 | `map_location='cpu'`, `weights_only=True` |
| `model.load_state_dict(state)` | 같은 구조 모델에 상태 적용 | `state_dict` | `strict=True` 기본; shape/키 불일치를 숨기지 않음 |

새로운 실습에서는 위의 옵션을 전부 외우지 않고 코드에 표시된 인자만 바꿉니다.

---
## 01. Optimizer 비교 · PPT 16쪽

파일: **`01_optimizer.py`**

### 목표와 작성할 부분

**B01**
SGD의 학습할 파라미터는 model.parameters()입니다. lr=0.01, momentum=0.0으로 만드세요.
학습률은 기본값에 기대지 않고 명시하며, 두 Optimizer 모두 weight_decay=0.0으로 비교합니다.


**B02**
AdamW를 같은 lr=0.01로 만드세요. weight_decay=0.0을 반드시 적으세요.
이번에는 감쇠 효과가 아닌 갱신 규칙을 비교합니다. 이 공통 lr이 두 알고리즘의 최적 lr이라는 뜻은 아닙니다.


### 실행
이 README가 있는 폴더에서 실행합니다.
```console
python 01_optimizer.py
```

### 예상 출력 · CPU 정답 실행 예
```text
SGD 20 epochs / valid loss: 0.484183
AdamW 20 epochs / valid loss: 0.307332
```

### 완료 기준과 설명
TODO가 요구하는 후보 수·값·출력 모양을 모두 확인하고, 아래 질문에 답하면 완료입니다. 단순 실행 종료만으로 완료가 아닙니다.

동일하게 유지한 조건 3가지를 쓰세요. 이 결과로 항상 우수한 Optimizer를 정할 수 있나요?

내 설명: ______________________________

---
## 02. 학습률 두 개 비교 · PPT 26쪽

파일: **`02_learning_rate.py`**

### 목표와 작성할 부분

**B03**
학습률 후보 두 개를 리스트로 쓰세요: 0.001, 0.01.
모델·seed·20 epochs·AdamW·weight_decay=0은 그대로 둡니다.


### 실행
이 README가 있는 폴더에서 실행합니다.
```console
python 02_learning_rate.py
```

### 예상 출력 · CPU 정답 실행 예
```text
lr: 0.001 처음 5개: [0.50841, 0.506854, 0.505305, 0.503762, 0.502226]
마지막 valid loss: 0.480205
lr: 0.01 처음 5개: [0.494631, 0.480118, 0.46654, 0.453585, 0.442029]
마지막 valid loss: 0.307332
```

### 완료 기준과 설명
TODO가 요구하는 후보 수·값·출력 모양을 모두 확인하고, 아래 질문에 답하면 완료입니다. 단순 실행 종료만으로 완료가 아닙니다.

첫 5회와 마지막 loss를 함께 보세요. 빠른 감소와 최종 결과는 같은 말인가요?

내 설명: ______________________________

---
## 03. Batch·Iteration·Epoch · PPT 36쪽

파일: **`03_batches.py`**

### 목표와 작성할 부분

**B04**
DataLoader(dataset, batch_size=6, shuffle=False)를 만드세요.
20개를 순서대로 나누면 6·6·6·2개입니다. dataset은 필수, batch_size와 shuffle은 선택 인자입니다.


### 실행
이 README가 있는 폴더에서 실행합니다.
```console
python 03_batches.py
```

### 예상 출력 · CPU 정답 실행 예
```text
iteration: 1 X: (6, 2) y: (6,)
iteration: 2 X: (6, 2) y: (6,)
iteration: 3 X: (6, 2) y: (6,)
iteration: 4 X: (2, 2) y: (2,)
한 epoch의 iteration: 4
```

### 완료 기준과 설명
TODO가 요구하는 후보 수·값·출력 모양을 모두 확인하고, 아래 질문에 답하면 완료입니다. 단순 실행 종료만으로 완료가 아닙니다.

20건, batch_size=6일 때 마지막 배치와 한 epoch의 갱신 횟수는?

내 설명: ______________________________

---
## 04. 학습곡선 읽기 · PPT 45쪽

파일: **`04_curves.py`**

### 목표와 작성할 부분

**B05**
valid_losses에서 가장 작은 값의 위치를 구하고 1을 더해 best_epoch에 넣으세요.
리스트 위치는 0부터, 여기서 출력할 epoch는 1부터 시작합니다.


### 실행
이 README가 있는 폴더에서 실행합니다.
```console
python 04_curves.py
```

### 예상 출력 · CPU 정답 실행 예
```text
best epoch: 11 최소 valid loss: 0.32
생성: practice04_curves.png
```

생성 파일: `practice04_curves.png`

### 완료 기준과 설명
TODO가 요구하는 후보 수·값·출력 모양을 모두 확인하고, 아래 질문에 답하면 완료입니다. 단순 실행 종료만으로 완료가 아닙니다.

11회 이후 train과 valid가 다르게 움직이는 이유를 한 문장으로 설명하세요.

내 설명: ______________________________

---
## 05. Dropout 모드 관찰 · PPT 55쪽

파일: **`05_dropout.py`**

### 목표와 작성할 부분

**B06**
Dropout을 평가 모드로 바꾸세요. dropout.eval()은 mode만 바꿉니다.
평가 모드의 Dropout은 입력을 그대로 전달하며, gradient 비활성화와는 별개의 기능입니다.


### 실행
이 README가 있는 폴더에서 실행합니다.
```console
python 05_dropout.py
```

### 예상 출력 · CPU 정답 실행 예
```text
train 1 [[2.0, 2.0, 2.0, 2.0], [0.0, 2.0, 0.0, 0.0]]
train 2 [[2.0, 2.0, 2.0, 2.0], [0.0, 0.0, 2.0, 0.0]]
train 3 [[2.0, 0.0, 0.0, 2.0], [2.0, 0.0, 2.0, 2.0]]
eval 1 [[1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0]]
eval 2 [[1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0]]
eval 3 [[1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0]]
```

### 완료 기준과 설명
TODO가 요구하는 후보 수·값·출력 모양을 모두 확인하고, 아래 질문에 답하면 완료입니다. 단순 실행 종료만으로 완료가 아닙니다.

train의 값이 0 또는 2인 이유와 eval의 값이 1인 이유를 설명하세요.

내 설명: ______________________________

---
## 06. BatchNorm의 모양과 통계 · PPT 65쪽

파일: **`06_batchnorm.py`**

### 목표와 작성할 부분

**B07**
model에 X를 넣어 output을 구하세요. 입력 (4,2)는 Linear에서 (4,8)이 됩니다.
BatchNorm1d(8)은 8개 특성의 통계를 유지합니다.


### 실행
이 README가 있는 폴더에서 실행합니다.
```console
python 06_batchnorm.py
```

### 예상 출력 · CPU 정답 실행 예
```text
입력: (4, 2) 출력: (4, 8)
running_mean: (8,)
eval에서 통계 유지: True
```

### 완료 기준과 설명
TODO가 요구하는 후보 수·값·출력 모양을 모두 확인하고, 아래 질문에 답하면 완료입니다. 단순 실행 종료만으로 완료가 아닙니다.

num_features=8은 입력의 행 수인가요, 앞 Linear의 출력 열 수인가요?

내 설명: ______________________________

---
## 07. 실습 07~08 · 학습 안정화 비교 · PPT 75,79쪽

파일: **`07_project.py`**

### 목표와 작성할 부분

**B08**
이미 zero_grad와 loss 계산이 끝났습니다. loss.backward() 다음 optimizer.step()을 호출하세요.
학습 데이터만 사용합니다. 비교 후보마다 모델을 처음부터 새로 만듭니다.


**B09**
한 epoch의 번호와 갱신 후 train_loss, valid_loss를 기록하세요.
history.append([epoch, train_loss, valid_loss]) 형태로 추가합니다.


### 실행
이 README가 있는 폴더에서 실행합니다.
```console
python 07_project.py
```

### 예상 출력 · CPU 정답 실행 예
```text
setting    lr  best_epoch  best_valid_loss
 baseline 0.001          20         0.480205
candidate 0.010          20         0.307332
test 미사용 / best epoch는 관찰한 최소 지점, 기본필수에서는 모델 저장·복원하지 않음
```

생성 파일: `history_baseline.csv`, `history_candidate.csv`, `experiment_table.csv`, `curves_baseline.png`, `curves_candidate.png`

### 완료 기준과 설명
TODO가 요구하는 후보 수·값·출력 모양을 모두 확인하고, 아래 질문에 답하면 완료입니다. 단순 실행 종료만으로 완료가 아닙니다.

바꾼 조건 하나, best epoch, 최종 해석과 한계를 각각 한 문장으로 쓰세요.

내 설명: ______________________________

---
## 실습 08 · 07번 결과를 다시 실행하고 설명하기
07번 파일을 **설정을 바꾸지 않고** 다시 실행합니다. 두 실험표와 곡선을 확인하고 다음 세 문장을 채웁니다.
1. 내가 고정한 조건은 ______이고 바꾼 것은 ______이다.
2. best valid loss는 ______, 해당 epoch는 ______이고, 마지막 값과의 차이는 ______이다.
3. 결과의 한계는 ______이며, 다음에는 test가 아닌 ______를 이용해 ______를 확인하겠다.

학습률을 바꾸는 추가 탐색을 이미 수행했다면 그 사실과 횟수도 기록합니다. 예제 숫자를 맞추려고 데이터를 수정하지 않습니다.

## 막혔을 때 확인
`ModuleNotFoundError`: VS Code 인터프리터가 전날 가상환경인지 확인합니다.
파일이 없다는 메시지: ZIP을 풀었는지, CSV를 지우지 않았는지 확인합니다.
Dropout 평가값이 변함: `.eval()`이 TODO로 남아 있는지 봅니다.
BatchNorm 크기 오류: 앞 Linear의 출력 열 수와 `num_features`가 같은지 봅니다.
PNG 창이 안 열림: 오류가 아닙니다. 저장된 PNG를 VS Code 파일 탐색기에서 엽니다.

미완성 코드를 실행하면 임시 값의 결과가 나올 수 있습니다. README의 후보 개수와 예상 결과를 비교합니다.

## 공식 참고자료
아래 링크는 인자·동작의 근거입니다. 버전에 따라 일부 인자가 다를 수 있어, 설치한 버전의 문서를 확인합니다.
- [SGD (검수 API 2.10)](https://docs.pytorch.org/docs/2.10/generated/torch.optim.SGD.html)
- [AdamW](https://docs.pytorch.org/docs/stable/generated/torch.optim.AdamW.html)
- [Dropout](https://docs.pytorch.org/docs/stable/generated/torch.nn.Dropout.html)
- [BatchNorm1d](https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm1d.html)
- [ReduceLROnPlateau](https://docs.pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.ReduceLROnPlateau.html)
- [CosineAnnealingLR](https://docs.pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.CosineAnnealingLR.html)
- [재현성](https://docs.pytorch.org/docs/stable/notes/randomness.html)
- [모델·Optimizer 저장 및 복원](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html)

## 선택: 오류 패턴별 처방 연습 (설명용 가상 상황)
아래는 실제 실행 수치가 아닌 진단 연습입니다. 원인을 확정하기보다 **먼저 확인할 근거**와 **한 번에 바꿀 조건 하나**를 씁니다.

|상황|관찰|내가 먼저 확인할 것|내 처방 후보|
|---|---|---|---|
|A|20회 동안 train·valid loss가 모두 거의 줄지 않음|||
|B|train loss는 0.6→0.1, valid loss는 0.5→0.8|||
|C|같은 입력인데 평가할 때마다 확률이 달라짐|||
|D|작은 batch에서 BatchNorm 사용 후 값이 크게 출렁임|||

기본필수는 한 상황만 말로 설명해도 됩니다. 복잡한 예외처리 코드를 추가하는 과제가 아닙니다.
