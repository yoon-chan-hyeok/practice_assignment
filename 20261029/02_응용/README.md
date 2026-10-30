# 응용 · Day9

직접 완성할 부분은 A01~A10의 10곳입니다. **코드는 한 파일씩, 입력은 data/, 결과는 outputs/**로 구분합니다. 사용자 정의 함수나 예외처리를 요구하지 않습니다. 기본필수보다 mini-batch·device 이동·기록을 연결합니다.

```text
02_응용/
  README.md
  01_environment.py ... 07_project.py
  data/points.csv
  outputs/                # 직접 실행하면 채워짐
```

실습01~06은 각각 단독 실행됩니다. 07은 앞 결과 파일을 요구하지 않는 제공 골격입니다. 08에서는 07을 재실행합니다. CUDA가 가능하면 GPU를 선택하고, 아니면 CPU로 실행합니다. 설치는 상위 README를 따릅니다.

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

## 01 · 환경과 CPU 대체 경로

**할 일:** 선택 device에 Tensor를 실제 이동하고 gpu_check.txt로 기록한다.

**A01** — CUDA를 사용할 수 있으면 cuda:0, 아니면 cpu를 선택하세요. 선택된 device는 아래 연산과 기록에 함께 사용합니다.

```powershell
python 01_environment.py
```

실제 CPU 예상 출력:

```text
torch: 2.10.0+cpu
cuda_build: None
cuda_available: False
selected_device: cpu
연산: [2.0, 3.0]
```

## 02 · reshape·broadcasting

**할 일:** (6,)→(2,3), bias (3,) 더하기, CPU/device 왕복을 확인한다.

**A02** — 원소 6개를 2행 3열로 바꾸어 matrix에 저장하세요. 아래 bias는 각 열에 더해집니다.

```powershell
python 02_tensor.py
```

실제 CPU 예상 출력:

```text
변환 전: (6,)
행렬: (2, 3) [[0.0, 1.0, 2.0], [3.0, 4.0, 5.0]]
보정 후: (2, 3) [[10.0, 21.0, 32.0], [13.0, 24.0, 35.0]]
이동 장치: cpu
CPU에서 확인: [[10.0, 21.0, 32.0], [13.0, 24.0, 35.0]]
```

## 03 · 수동 파라미터 갱신

**할 일:** 목표4, lr0.1, 10step의 갱신 후 w와 loss를 기록한다.

**A03** — w에서 학습률 × 현재 기울기를 빼세요. 여기는 no_grad 블록 안입니다. 새 값으로 Tensor 객체를 교체하지 말고 w를 직접 갱신하세요.

```powershell
python 03_gradient_descent.py
```

실제 CPU 예상 출력:

```text
1 0.8 10.240001
2 1.44 6.5536
3 1.952 4.194304
4 2.3616 2.684354
5 2.68928 1.717987
6 2.951424 1.099511
7 3.161139 0.703687
8 3.328911 0.45036
9 3.463129 0.28823
10 3.570503 0.184467
```

## 04 · 은닉 너비와 파라미터

**할 일:** 은닉4·8·16의 출력 shape와 파라미터22·42·82를 비교한다. 성능 순위는 비교하지 않는다.

**A04** — hidden 값을 사용해 입력 2개 → 은닉 hidden개 → 출력 2개를 연결하세요. 은닉층 뒤에 ReLU를 넣고 마지막에 softmax는 넣지 않습니다.

```powershell
python 04_ann.py
```

실제 CPU 예상 출력:

```text
은닉: 4 출력: (4, 2) 파라미터: 22
은닉: 8 출력: (4, 2) 파라미터: 42
은닉: 16 출력: (4, 2) 파라미터: 82
```

## 05 · 마지막 작은 batch

**할 일:** 정상10건을4·4·2로 읽고 합계10을 확인한다. num_workers=0을 유지한다.

**A05** — dataset을 batch_size=4, shuffle=False, drop_last=False로 공급하세요. 정상 데이터 10건이 4·4·2로 나뉘어야 합니다. num_workers=0을 유지합니다.

```powershell
python 05_batches.py
```

실제 CPU 예상 출력:

```text
1 (4, 2) (4,)
2 (4, 2) (4,)
3 (2, 2) (2,)
합계: 10
예시 CE: 0.126928
```

## 06 · mini-batch 학습 기록

**할 일:** train120을batch32로 80epoch 학습하고 10epoch마다 train/valid 지표를 기록한다.

**A06** — 현재 batch의 loss로 역전파하고 optimizer를 한 번 갱신하세요. zero_grad와 순전파·손실 계산은 위에 제공되어 있습니다.

```powershell
python 06_train.py
```

실제 CPU 예상 출력:

```text
0 0.565832 0.510637 0.7
10 0.331469 0.281476 0.975
20 0.228078 0.182579 0.975
30 0.176405 0.134341 1.0
40 0.145632 0.105641 1.0
50 0.12504 0.086818 1.0
60 0.110228 0.074174 1.0
70 0.098804 0.064484 1.0
80 0.089844 0.057217 1.0
```

## 07 · 한 파일 프로젝트

**할 일:** 환경·학습·평가·CSV/JSON 저장을 연결한다. test40은 보관한다.

**A07** — 각 batch에서 backward와 step을 연결하세요. train 자료만 loader에 들어갑니다. valid로 backward하거나 학습하지 마세요.

**A08** — logits의 클래스 축에서 가장 큰 점수의 인덱스를 구하세요. CSV로 저장하기 전에 CPU로 옮깁니다. y_valid의 순서는 그대로 유지하세요.

```powershell
python 07_project.py
```

실제 CPU 예상 출력:

```text
0 0.565832 0.510637 0.7
10 0.331469 0.281476 0.975
20 0.228078 0.182579 0.975
30 0.176405 0.134341 1.0
40 0.145632 0.105641 1.0
50 0.12504 0.086818 1.0
60 0.110228 0.074174 1.0
70 0.098804 0.064484 1.0
80 0.089844 0.057217 1.0
생성: outputs의 환경·학습·검증 결과
```

## 실습 08 · 재현·설명

`python 07_project.py`를 다시 실행합니다. `outputs/`의 `gpu_check.txt`, `training_history.csv`, `final_metrics.json`, `validation_predictions.csv`를 확인합니다. train120 / valid40 / test40(미사용)을 유지합니다. 이 자료의 학습 120건은 batch32·32·32·24로 나뉩니다.

CSV 기록의 `train_loss_eval`은 해당 epoch 갱신을 모두 끝낸 뒤 train 전체를 다시 평가한 손실입니다. 마지막 작은 batch의 loss 하나를 전체 loss처럼 기록하지 않습니다. `epoch=0`은 학습 전입니다.

### 이번에 추가로 읽는 인자

| 호출 | 필수 | 선택·이 수업의 값 | 의미 |
|---|---|---|---|
| `Tensor.reshape(2,3)` | 새 모양 | `-1` 한 곳은 자동 계산 가능 | 원소 수6 유지 |
| `TensorDataset(X,y)` | 묶을 Tensor들 | 이번 예제는2개 | 첫 차원의 길이가 같아야 함 |
| `DataLoader(dataset,...)` | dataset | batch_size32, shuffle=True, num_workers0, drop_last=False | 작은 묶음을 순회 |
| `torch.Generator().manual_seed(43)` | manual_seed의 seed | CPU Generator 사용 | shuffle 전용 난수 흐름 |
| `nn.CrossEntropyLoss()` | 생성시 없음 | reduction="mean" | batch 평균 손실 |
| `loss_fn(logits,y)` | logits,y | class index y는long | gradient가 이어지는 스칼라 |

### 내 설명

- full-batch와 mini-batch의 차이: 
- 마지막 batch가 작을 수 있는 이유: 
- 입력·정답·모델을 같은 device에 두는 이유: 
- 수동 갱신 뒤 loss와 갱신 전 loss를 구분하는 이유: 
- 이번 valid 결과의 한계: 

제출은 코드·data·outputs와 이 설명입니다. 별도 모듈·테스트 파일을 추가할 필요는 없습니다.


## 추가 A09 · 05번의 배치 손실 집계

05_batches.py에서 평균 손실 `[0.1, 0.2, 0.9]`와 실제 배치 크기 `[4,4,2]`를 사용합니다. 각 평균×표본수의 합을 전체 표본 수로 나눕니다. **가중 평균 0.3**, 잘못된 단순 평균 **0.4**를 비교합니다. 새 함수나 폴더는 만들지 않습니다.

## 추가 A10 · 07~08번의 오답 기록

07_project.py에서 valid ID·실제값·예측값을 같은 순서로 묶고 다른 행만 남깁니다. `outputs/validation_errors.csv`의 헤더는 `id,actual,predicted`입니다. 오답이 없으면 헤더만 있는 파일을 만듭니다.

완료 기준: 저장한 오답 행 수가 valid 40건에서 맞힌 개수를 뺀 수와 같습니다. 원본과 test를 수정하지 않습니다. 기본 CPU 예제에서는 오답 0건이므로 가상의 오답을 추가하지 않습니다. 평가 표본이 작고 합성 규칙이 단순함을 기록합니다.

### 새 함수·반환값 읽기
`zip(a,b,c)`는 같은 위치의 원소를 묶습니다. 가장 짧은 길이에서 멈추므로 제공된 세 자료의 동일한 valid 순서를 유지해야 합니다. `int(tensor_scalar)`는 CSV에 쓸 정수로 바꿉니다. 이 단계의 TODO는 새 사용자 정의 함수를 요구하지 않습니다.
