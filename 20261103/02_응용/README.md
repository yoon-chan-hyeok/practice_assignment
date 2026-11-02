# 응용 · Mask와 비교 실험 연결

코드8개·README, 입력 `data/`, 생성 결과 `outputs/`만 사용한다. 사용자 정의 함수·클래스를 추가로 만들지 않는다. 직접 구현은 TODO10곳이다. 실습08에서 최적 모델 복원·클래스별 Recall·오답 기록을 추가한다. 제공된 반복 학습/출력 부분은 읽되 모두 다시 작성하지 않는다.

```
02_응용/
  README.md
  01_mask.py ... 08_project.py
  data/series.csv
  data/sequences.json
  outputs/  # 실행으로 생성
```

01~07은 독립 실행이다. **08은 분류 비교를 통합**한다. 전체 산출물은 다음 세 명령으로 구성한다. 시계열·재구성 지표와 분류 지표를 한 점수로 합치지 않는다.

```powershell
python 03_forecast.py
python 04_latent.py
python 08_project.py
```

03·04의 결과가 없어도 08 자체는 실행된다. 08이 기존 표를 몰래 정답 파일에서 복사하지 않는다. 저장 모델은 08이 생성한다. 복원 구현은 심화에서 다룬다. 07은 GPU가 없으면 CUDA 행을 NOT_AVAILABLE로 남기고 CPU 결과만 기록한다.

## 데이터와 분할

이번에는 이미지 대신 새로 만든 정상 사인파·독립 Sequence를 사용한다. 기존 요청 로그와 이미지 자료를 재사용한 것은 아니다. 모든 파일은 UTF-8이다. 결측·중복 ID·잘못된 값 정제는 이번 필수 과제가 아니다.

| 자료 | 기본필수 | 응용·심화·특심화 | 사용 방법 |
|---|---|---|---|
| `series.csv` | 시간순 원관측 100개:60/20/20 | 원관측300개:180/60/60 | 각 시간 구간 안에서 Window 생성 |
| 과거12→다음1 | train48·valid8 | train168·valid48 | test Window는 만들지 않음 |
| 8차원 재구성 | train53·valid13 | train173·valid53 | target=입력8개; Denoising은 clean을 target으로 유지 |
| 독립 Sequence 분류 | 06번 코드의20개:12/4/4 | `sequences.json`100개:60/20/20 | 증가1·감소0, 길이6~12·특성3, ID 기준 독립 |

사인파는 `sin(time*0.23)+0.15*cos(time*0.071)`로 생성했다. 학습용 단순 합성 신호이지 실제 센서의 예측 성능이 아니다. **시간 구간을 먼저 분리하고 그 안에서만 Window를 만든다.** 경계를 넘는 Window와 무작위 Window 분할은 사용하지 않는다. 예측은 이전 관측이 순차적으로 도착하는 one-step 방식이며 여러 시점 재귀 예측과 다르다.

분류 Sequence는 평균이 아니라 증가/감소 순서를 학습하도록 생성했다. 한 시퀀스 안의 시점을 섞지 않는다. 독립 Sequence 사이의 학습 배치 shuffle과 구분한다. `test` 구간/ID는 공통 실습의 학습·선택·예측에 전달하지 않는다.

특심화 **선택 이상탐지 과제만 예외**다. 별도로 생성한 정상 train80·정상/이상 valid40·test40을 사용한다. 정상train으로 AE 학습 → valid로 임계값 확정 → 설정 저장 → 별도 명령으로 해당 test를 한 번 평가한다. 공통 시계열·분류 test를 사용하는 것이 아니다.

## 새 함수·클래스 읽는 법

괄호를 쓰는 **층 생성**과 **데이터 계산**은 다르다. `rnn=nn.RNN(...)`은 층을 만들고, `output,h=rnn(x)`는 실제 계산이다.

| 호출 | 역할 | 필수 인자 | 주요 선택 인자·기본값 / 반환 |
|---|---|---|---|
| `pad_sequence(sequences, ...)` | 서로 다른 길이를 한 배치로 채움 | Tensor 목록 `sequences` | `batch_first=False`, `padding_value=0.0`; 여기서는 True → `[B,T,F]` |
| `nn.RNN(input_size, hidden_size, ...)` | 이전 상태를 다음 시점으로 전달 | 시점별 특성 수, 은닉 크기 | `num_layers=1`, `batch_first=False`, `nonlinearity='tanh'` |
| `rnn(input, hx=None)` | RNN 순전파 | 입력 | 초기 상태 생략 시 0; `output`, `h_n` 반환 |
| `nn.LSTM(input_size, hidden_size, ...)` | hidden과 cell state를 유지 | 특성 수, 은닉 크기 | `num_layers=1`, `batch_first=False`, `dropout=0`, `bidirectional=False` |
| `lstm(input, hx=None)` | LSTM 순전파 | 입력 | 선택 hx=`(h0,c0)`; 반환 `output,(h_n,c_n)` |
| `nn.Linear(in_features,out_features)` | 마지막 축을 새 특성 수로 변환 | 입력·출력 특성 수 | `bias=True`; `[B,T,H]`도 마지막 H축에 적용 |
| `tensor.unfold(dimension,size,step)` | 관측 Window 뷰 생성 | 축·Window 크기·이동 폭 | 본 실습 `(0,13,1)`은 과거12+다음정답1 |
| `nn.MSELoss()` | 제곱오차 평균 | 생성 시 필수 없음; 계산 시 예측·정답 | `reduction='mean'`; 두 Tensor shape를 같게 준비 |
| `nn.MultiheadAttention(embed_dim,num_heads,...)` | 위치 간 가중합 | 표현 크기, head 수 | `dropout=0`, `batch_first=False`; 표현 크기는 head 수로 나누어져야 함 |
| `attention(query,key,value,...)` | Attention 계산 | Q·K·V 입력 | `key_padding_mask=None`, `need_weights=True`, `average_attn_weights=True` |
| `nn.TransformerEncoderLayer(d_model,nhead,...)` | Attention+FFN 블록 | 표현 크기·head 수 | `dim_feedforward=2048`, `dropout=0.1`, `batch_first=False`; 여기서는 작은 FFN·dropout0 지정 |
| `nn.TransformerEncoder(layer,num_layers,...)` | Encoder 층 묶음 | layer·층 수 | 본 자료는 1층·`enable_nested_tensor=False` |
| `nn.Embedding(num_embeddings,embedding_dim)` | 위치 번호를 벡터로 변환 | 위치 수·벡터 크기 | `padding_idx=None`; 학습 가능한 위치 표현을 더함 |
| `pack_padded_sequence(input,lengths,...)` | Padding 없는 압축 표현 | 입력·각 실제 길이 | `batch_first=False`, `enforce_sorted=True`; CPU int64 길이 사용 |
| `pad_packed_sequence(sequence,...)` | 압축 표현을 Tensor로 복원 | PackedSequence | `batch_first=False`, `total_length=None`; `(padded,lengths)` 반환 |

`batch_first=True`여도 `h_n`, `c_n`은 `[layers×directions,B,H]`다. 기본 예제는 1층·단방향이다. `output[:,-1]`은 **고정 길이에만** 마지막 실제 시점이다. 가변 길이는 lengths/packed를 사용한다. LSTM의 `dropout`은 층 사이에 적용되므로 1층에서 규제를 넣으려면 별도 Dropout 등을 설계한다.

이 자료의 `nn.MultiheadAttention`/Transformer bool Mask에서 **True는 제외**다. 다른 Attention API의 bool 의미까지 같다고 일반화하지 않는다. key Mask를 넣어도 padded query 출력이 자동으로 0이 되지는 않으므로 평균 집계에서도 제외한다.

## 01_mask.py · 길이 기반 Mask와 평균

PPT 12쪽과 연결한다. 터미널 위치는 이 응용 폴더로 둔다.

```powershell
python 01_mask.py
```

### 직접 완성할 부분

- **A01**: Padding이 아닌 실제 시점만 합산하고 각 자료의 실제 길이로 나눈다. 힌트: mask=True는 Padding이다. 0도 정상 관측값일 수 있으므로 값이 0인지로 판정하지 않는다.

### 실행 결과 확인

```text
Padding mask:
 tensor([[False, False, False, False,  True],
        [False, False,  True,  True,  True],
        [False, False, False, False, False]])
실제 값 평균:
 tensor([[1., 1., 1.],
        [2., 2., 2.],
        [3., 3., 3.]])
```

생성 파일: `outputs/padding_mask.csv`

**완료 기준**: Padding 포함 평균과 실제 길이로 나눈 평균을 비교한다.

### 자신의 말로 설명하기

- B·T·F가 각각 무엇인가? → 답: ____________________
- Padding의 0과 실제 관측값0을 어떻게 구분하는가? → 답: ____________________

## 02_outputs.py · Sequence-to-one·many

PPT 22쪽과 연결한다. 터미널 위치는 이 응용 폴더로 둔다.

```powershell
python 02_outputs.py
```

### 직접 완성할 부분

- **A02**: 모든 시점의 hidden을 같은 Linear 층에 넣어 시점별 logits를 만든다. 힌트: Linear는 마지막 차원에 적용되므로 [B,T,H]→[B,T,C]로 작동한다.

### 실행 결과 확인

```text
one: (4, 2) many: (4, 6, 2)
마지막 logits 일치: True
같은 Head를 시점마다 재사용하며, 시점별 정답은 별도 설계가 필요하다.
```

**완료 기준**: 전체 시점 출력과 마지막 시점만 선택하는 차이를 설명한다.

### 자신의 말로 설명하기

- output과 h_n의 차이는? → 답: ____________________
- 모든 시점의 logits를 쓰려면 어떤 정답 구조가 필요한가? → 답: ____________________

## 03_forecast.py · RNN·LSTM 다음 값 비교

PPT 34쪽과 연결한다. 터미널 위치는 이 응용 폴더로 둔다.

```powershell
python 03_forecast.py
```

### 직접 완성할 부분

- **A03**: 각 과거 Window의 마지막 출력에서 다음 값에 대한 MSE를 계산한다.

### 실행 결과 확인

```text
windows: 168 48 test 미사용
      model  hidden  params  epochs  best_epoch  valid_mse
        RNN       8      97      40          39   0.002789
       LSTM       8     361      40          40   0.001272
Persistence       0       0       0           0   0.026131
```

생성 파일: `outputs/forecast_comparison.csv`

**완료 기준**: MSE가 persistence보다 좋은지 확인한다. hidden 동일은 Params 동일이 아니다.

### 자신의 말로 설명하기

- 과거12개 중 정답이 섞여 있지는 않은가? → 답: ____________________
- LSTM의 h와 c를 구분할 수 있는가? → 답: ____________________

## 04_latent.py · Latent 크기 비교

PPT 47쪽과 연결한다. 터미널 위치는 이 응용 폴더로 둔다.

```powershell
python 04_latent.py
```

### 직접 완성할 부분

- **A04**: 후보 latent_size=1·2·4를 실제 Encoder·Decoder 크기에 적용한다.

### 실행 결과 확인

```text
latent  retained_ratio  params  best_epoch  valid_mse
      1           0.125      25          40   0.157463
      2           0.250      42          40   0.176410
      4           0.500      76          40   0.009960
```

생성 파일: `outputs/latent_comparison.csv`

**완료 기준**: latent/8은 차원 비율이며 실제 파일 압축률·이상탐지 성능이 아니다.

### 자신의 말로 설명하기

- 예측의 target과 재구성의 target은 어떻게 다른가? → 답: ____________________
- 재구성 오류가 높다고 무조건 이상인가? → 답: ____________________

## 05_attention_mask.py · Attention Padding Mask

PPT 58쪽과 연결한다. 터미널 위치는 이 응용 폴더로 둔다.

```powershell
python 05_attention_mask.py
```

### 직접 완성할 부분

- **A05**: Padding을 key로 보지 않게 bool Mask를 전달한다. 힌트: nn.MultiheadAttention의 key_padding_mask: [B,T], True가 제외 위치이다.

### 실행 결과 확인

```text
shape: (2, 5, 16) (2, 4, 5, 5)
막은 key weight 최대: 0.0
유효 query 출력 변화: 0.27656
masked mean: (2, 16)
```

생성 파일: `outputs/mask_or_latent.png`

**완료 기준**: key 차단과 padded query 제외를 구분한다.

### 자신의 말로 설명하기

- key Padding과 query 집계 제외를 왜 둘 다 하는가? → 답: ____________________
- head별 weight와 head 평균 weight의 shape 차이는? → 답: ____________________

## 06_transformer.py · Position·Mask를 사용한 Transformer

PPT 70쪽과 연결한다. 터미널 위치는 이 응용 폴더로 둔다.

```powershell
python 06_transformer.py
```

### 직접 완성할 부분

- **A06**: Transformer에 실제 길이로 만든 Padding Mask를 전달한다. 힌트: 위치 임베딩은 값 임베딩과 더한다. masked mean에서는 Padding query도 제외한다.

### 실행 결과 확인

```text
train/valid: 60 20 위치 최대 길이: 12
params: 746
valid accuracy: 1.0
```

생성 파일: `outputs/transformer_predictions.csv`

**완료 기준**: 길이 평균에서 Padding 제외, 위치 정보와 라벨 분할을 설명한다.

### 자신의 말로 설명하기

- 같은 hidden 크기면 파라미터 수도 같은가? → 답: ____________________
- 분류 accuracy와 재구성 MSE를 평균내면 왜 안 되는가? → 답: ____________________

## 07_device_time.py · CPU/GPU 순전파 비교

PPT 81쪽과 연결한다. 터미널 위치는 이 응용 폴더로 둔다.

```powershell
python 07_device_time.py
```

### 직접 완성할 부분

- **A07**: CUDA 측정 종료 전에 비동기 작업의 완료를 기다린다. 힌트: CPU에는 synchronize를 호출하지 않는다. 시작 직전 동기화는 제공되어 있다.

### 실행 결과 확인

아래 값 중 시간·처리량은 검수 PC의 관측 예시이다. **정답 숫자로 맞추지 않는다.** 같은 모델·데이터라도 실행 부하로 달라진다.

```text
device        status  seconds     samples_s peak_bytes
   cpu            OK 0.002636 182088.072212       None
  cuda NOT_AVAILABLE      NaN           NaN       None
동일 초기상태·입력 / forward 30회 / H2D·DataLoader·backward 제외 / VRAM=모델+입력 포함 allocated peak
```

생성 파일: `outputs/device_time.csv`

**완료 기준**: 측정 범위와 미측정 GPU의 N/A를 명확히 적는다.

### 자신의 말로 설명하기

- 측정에 forward/backward/H2D/로딩 중 무엇이 포함됐나? → 답: ____________________
- CPU에서 VRAM을0이 아니라 N/A로 적는 이유는? → 답: ____________________

## 08_project.py · 응용 분류 비교 통합

PPT 87쪽과 연결한다. 터미널 위치는 이 응용 폴더로 둔다.

```powershell
python 08_project.py
```

### 직접 완성할 부분

- **A08**: Packed LSTM의 실제 마지막 상태를 분류 Head에 전달한다. 힌트: Packed output.data는 순서가 다른 압축된 모든 시점이다. h[-1]은 원래 배치 순서의 마지막 상태이다.

### 실행 결과 확인

아래 값 중 시간·처리량은 검수 PC의 관측 예시이다. **정답 숫자로 맞추지 않는다.** 같은 모델·데이터라도 실행 부하로 달라진다.

```text
model  params  best_epoch  valid_loss  valid_accuracy
       LSTM     434          30    0.039391             1.0
Transformer     746          30    0.008062             1.0
시계열·재구성 비교표: 03_forecast.py와 04_latent.py를 실행해 함께 제출
test: 학습·평가 미사용
```

생성 파일: `outputs/architecture_comparison.csv`, `outputs/classification_history.csv`, `outputs/classification_predictions.csv`

**완료 기준**: LSTM·Transformer의 파라미터 수·입력 길이·loss·정확도·시간의 차이를 설명한다.

### 자신의 말로 설명하기

- best epoch를 train과 valid 중 어디에서 골랐나? → 답: ____________________
- test를 사용한 곳이 있는가? → 답: ____________________
- 다음 값 예측과 재구성 모델의 오류 사례·한계를 구분했나? → 답: ____________________

## 최종 설명란

- 예측·재구성·분류의 target과 metric: ____________________
- 같은 분할·epoch·학습률과 서로 다른 파라미터 수: ____________________
- Mask가 차단하는 위치와 pooled 평균에서 제외할 위치: ____________________
- 실제 측정 장치·범위 / GPU 미측정 여부: ____________________
- test 미사용과 한계: ____________________

## 최신 수정판 추가 과제 · A09~A10 (실습 08)

A09는 `08_project.py`에서 최저 valid loss의 `best_state`를 복원합니다. 출력의 `최적 모델 출력 일치: True`를 두 모델에서 확인하세요. A10은 실제 표본 수와 정답 수로 클래스별 Recall을 계산하고 **틀린 표본만** 기록합니다. `outputs/class_metrics.csv`는 2모델×2클래스=4행입니다. `error_samples.csv`는 오답이 없을 때 헤더만 있는 것이 정상입니다. 실행을 끝내는 것과 TODO를 완성하는 것은 다릅니다. `pass`를 남겼다면 예상 행 수가 맞지 않을 수 있습니다.

추가 함수나 하위 폴더는 없습니다. 분류·예측·재구성은 서로 다른 목표이므로 지표를 합쳐 평균내지 않습니다.
