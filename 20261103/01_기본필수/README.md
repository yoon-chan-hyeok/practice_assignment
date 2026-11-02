# 기본필수 · 짧은 코드로 Sequence 모델 익히기

**Python 8개 + 정상 CSV1개 + 이 README**만 있다. 하위 폴더·사용자 정의 함수·클래스·예외처리가 없다. 모델을 처음부터 설계하지 말고 제공된 흐름에서 TODO9곳을 완성한다.

| 교시 | 파일 | 할 일 |
|---|---|---|
| 1 | 01_padding.py | 실제 길이가 다른 자료를 배치로 묶기 |
| 2 | 02_rnn.py | output·h_n·logits 구분 |
| 3 | 03_lstm.py | 과거12개→다음값1개의 Shape |
| 4 | 04_autoencoder.py | 8→2→8 재구성 |
| 5 | 05_attention.py | head별 Attention Shape |
| 6 | 06_compare.py | 작은 정상 Sequence의 RNN·LSTM 학습 |
| 7 | 07_benchmark.py | CPU forward 시간·처리량 |
| 8 | 08_project.py | LSTM 예측+AE 재구성·결과 저장 |

01~07은 다른 파일의 결과가 없어도 실행된다. 08도 자신의 원본 CSV에서 다시 시작한다. 마지막 프로젝트는 제공된 긴 연결 코드 중 **B08·B09 두 곳**만 수정한다. 저장·그림·best 상태 코드는 제공한다.

PPT보다 모델을 작게 쓴다: RNN/LSTM hidden8, Attention16·head4, AE8→2→8. 기본필수 분류는 코드 안의 정상20개·train12/valid4/test4다. 과거 이미지나 요청 로그의 숫자와 맞추는 과제가 아니다.

원본 CSV100개를 시간순60/20/20으로 먼저 나누어 각각 Window를 만든다. 예측 train48/valid8, 재구성train53/valid13이 된다. **train/valid 사이 원본 시점이 겹치지 않는다.** test구간은 보관한다.

학습 전 03의 수치는 낮은 오차를 요구하지 않는다. 06의 정확도1.0도 손쉬운 합성 시퀀스20개에 대한 관측이다. 04와08의 MSE는 목표·Window가 다르므로 억지로 하나의 순위로 만들지 않는다.

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

## 01_padding.py · Sequence와 Padding

PPT 12쪽과 연결한다. 터미널 위치는 이 기본필수 폴더로 둔다.

```powershell
python 01_padding.py
```

### 직접 완성할 부분

- **B01**: B가 첫 축인 [3,5,3] Padding Tensor를 만든다. 힌트: batch_first의 기본값은 False이다. 여기서는 True로 바꾼다.

### 실행 결과 확인

```text
입력 길이: [4, 2, 5]
Padding shape: (3, 5, 3)
두 번째 자료:
 tensor([[2., 2., 2.],
        [2., 2., 2.],
        [0., 0., 0.],
        [0., 0., 0.],
        [0., 0., 0.]])
```

**완료 기준**: B·T·F와 채워진 0의 위치를 설명한다.

### 자신의 말로 설명하기

- B·T·F가 각각 무엇인가? → 답: ____________________
- Padding의 0과 실제 관측값0을 어떻게 구분하는가? → 답: ____________________

## 02_rnn.py · RNN과 출력 Shape

PPT 22쪽과 연결한다. 터미널 위치는 이 기본필수 폴더로 둔다.

```powershell
python 02_rnn.py
```

### 직접 완성할 부분

- **B02**: 은닉 특성 8개를 두 클래스의 점수로 바꾸는 층을 만든다. 힌트: 필수 위치 인자: in_features=8, out_features=2; bias=True는 기본 선택값.

### 실행 결과 확인

```text
입력: (4, 6, 3)
output / h_n: (4, 6, 8) (1, 4, 8)
logits: (4, 2)
마지막 시점 일치: True
```

**완료 기준**: [4,6,8]과 [1,4,8]의 차이, logits가 확률이 아닌 점수를 설명한다.

### 자신의 말로 설명하기

- output과 h_n의 차이는? → 답: ____________________
- 모든 시점의 logits를 쓰려면 어떤 정답 구조가 필요한가? → 답: ____________________

## 03_lstm.py · LSTM 다음 값 예측

PPT 34쪽과 연결한다. 터미널 위치는 이 기본필수 폴더로 둔다.

```powershell
python 03_lstm.py
```

### 직접 완성할 부분

- **B03**: 12개 관측의 마지막 은닉 출력으로 다음 값 1개를 예측한다. 힌트: [:, -1, :]는 마지막 시점이다. 이 예제의 Window 길이는 모두 12이다.

### 실행 결과 확인

```text
입력 / 정답: (48, 12, 1) (48, 1)
h_n / c_n: (1, 48, 8) (1, 48, 8)
예측: (48, 1)
첫 예측: 0.014645
학습 전 MSE: 0.374487
```

**완료 기준**: 아직 학습하지 않은 예측과 정답, h·c의 차이를 설명한다.

### 자신의 말로 설명하기

- 과거12개 중 정답이 섞여 있지는 않은가? → 답: ____________________
- LSTM의 h와 c를 구분할 수 있는가? → 답: ____________________

## 04_autoencoder.py · 8→2→8 재구성

PPT 47쪽과 연결한다. 터미널 위치는 이 기본필수 폴더로 둔다.

```powershell
python 04_autoencoder.py
```

### 직접 완성할 부분

- **B04**: Autoencoder의 정답을 입력 x 자체로 설정한다. 힌트: 정상 데이터를 0으로 바꾸는 과제가 아니다. reconstruction과 x를 비교한다.

### 실행 결과 확인

```text
train: (53, 8) valid: (13, 8)
latent / 복원: (13, 2) (13, 8)
valid MSE: 0.056042
```

**완료 기준**: 입력 자체가 정답임을 설명한다. 작은 latent가 오류 0을 보장하지 않는다.

### 자신의 말로 설명하기

- 예측의 target과 재구성의 target은 어떻게 다른가? → 답: ____________________
- 재구성 오류가 높다고 무조건 이상인가? → 답: ____________________

## 05_attention.py · Self-Attention Shape

PPT 58쪽과 연결한다. 터미널 위치는 이 기본필수 폴더로 둔다.

```powershell
python 05_attention.py
```

### 직접 완성할 부분

- **B05**: 4개 head의 가중치를 평균내지 않고 각각 받는다. 힌트: query/key/value에는 같은 x를 넣는다. average_attn_weights=False를 지정한다.

### 실행 결과 확인

```text
입력: (2, 5, 16)
출력: (2, 5, 16)
head별 weight: (2, 4, 5, 5)
각 행의 합: tensor([1., 1., 1., 1., 1.])
```

**완료 기준**: [2,4,5,5]의 각 축과 한 query가 모든 key를 비교하는 의미를 설명한다.

### 자신의 말로 설명하기

- key Padding과 query 집계 제외를 왜 둘 다 하는가? → 답: ____________________
- head별 weight와 head 평균 weight의 shape 차이는? → 답: ____________________

## 06_compare.py · RNN·LSTM 작은 분류 비교

PPT 70쪽과 연결한다. 터미널 위치는 이 기본필수 폴더로 둔다.

```powershell
python 06_compare.py
```

### 직접 완성할 부분

- **B06**: 손실의 gradient를 구한 뒤 모델과 head를 갱신한다. 힌트: backward가 gradient를 계산하고 optimizer.step이 가중치를 바꾼다.

### 실행 결과 확인

```text
RNN params: 106 valid 정답: [0, 1, 0, 1] 예측: [0, 1, 0, 1] accuracy: 1.0
LSTM params: 370 valid 정답: [0, 1, 0, 1] 예측: [0, 1, 0, 1] accuracy: 1.0
```

**완료 기준**: 동일 자료·epoch·은닉크기여도 파라미터 수가 다름을 설명한다.

### 자신의 말로 설명하기

- 같은 hidden 크기면 파라미터 수도 같은가? → 답: ____________________
- 분류 accuracy와 재구성 MSE를 평균내면 왜 안 되는가? → 답: ____________________

## 07_benchmark.py · CPU 순전파 시간

PPT 81쪽과 연결한다. 터미널 위치는 이 기본필수 폴더로 둔다.

```powershell
python 07_benchmark.py
```

### 직접 완성할 부분

- **B07**: 반복 전체에서 처리한 샘플 수를 경과 시간으로 나눈다. 힌트: 초당 샘플 수 = batch 수 × 반복 수 / 초. 숫자는 PC마다 달라진다.

### 실행 결과 확인

아래 값 중 시간·처리량은 검수 PC의 관측 예시이다. **정답 숫자로 맞추지 않는다.** 같은 모델·데이터라도 실행 부하로 달라진다.

```text
범위: CPU / forward만 / gradient 없음 / B=16,T=12,F=3
반복: 30 경과 초: 0.002691
samples/s: 178353.93
GPU peak VRAM: N/A (이 파일은 CPU 전용)
```

**완료 기준**: 추론 시간이지 학습 한 epoch 시간이 아님을 설명한다.

### 자신의 말로 설명하기

- 측정에 forward/backward/H2D/로딩 중 무엇이 포함됐나? → 답: ____________________
- CPU에서 VRAM을0이 아니라 N/A로 적는 이유는? → 답: ____________________

## 08_project.py · LSTM·AE 미니 프로젝트

PPT 87쪽과 연결한다. 터미널 위치는 이 기본필수 폴더로 둔다.

```powershell
python 08_project.py
```

### 직접 완성할 부분

- **B08**: LSTM의 마지막 관측 상태에서 다음 값을 계산한다.
- **B09**: 재구성의 target을 과거 8개 값인 ax로 지정한다.

### 실행 결과 확인

```text
forecast windows: 48 8 best epoch: 37
AE windows: 53 13 best epoch: 40
          task  best_epoch  valid_mse
      forecast          37   0.000003
reconstruction          40   0.056042
저장: history.csv / predictions.csv / reconstruction.csv / comparison.csv / best_model.pt / mask_or_latent.png
test 구간: 보관 / 평가하지 않음
```

생성 파일: `history.csv`, `predictions.csv`, `reconstruction.csv`, `comparison.csv`, `mask_or_latent.png`

**완료 기준**: 예측과 재구성의 target·MSE를 구분하고 best epoch·test 보관을 설명한다.

### 자신의 말로 설명하기

- best epoch를 train과 valid 중 어디에서 골랐나? → 답: ____________________
- test를 사용한 곳이 있는가? → 답: ____________________
- 다음 값 예측과 재구성 모델의 오류 사례·한계를 구분했나? → 답: ____________________

## 최종 제출·설명

코드8개·`history.csv`·`predictions.csv`·`reconstruction.csv`·`comparison.csv`·`mask_or_latent.png`를 확인한다. 자신이 생성한 best_model.pt는 같은 실험을 보관하는 파일이며 다시 모델을 선택하는 자료가 아니다. `.pt`는 재배포할 때 용량·신뢰를 확인한다.

위 08번 설명란에 **예측과 재구성의 차이 / best epoch 선택 근거 / 작은 합성 자료의 한계**를 3문장 이상 작성한다. 자동 테스트나 별도 보고서 파일 작성은 기본필수 과제가 아니다. 실행 후 valid 실제값과 예측을 대조한다.
