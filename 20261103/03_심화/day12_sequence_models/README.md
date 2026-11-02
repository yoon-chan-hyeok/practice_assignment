# day12_sequence_models · 시계열 예측·재구성·분류 비교

이 프로젝트 폴더만 다른 위치로 복사해도 실행할 수 있다. 데이터가 이 폴더에도 포함되어 있다. `models.py`·`data.py`·`train.py`는 제공 모듈이며 주된 TODO는 main2곳·restore1곳이다.

```
day12_sequence_models/
  README.md
  main.py          # 실험 실행·저장
  models.py        # 모델의 입력·출력
  data.py          # 시간 Window·Mask·데이터 읽기
  train.py         # train/evaluate·best 선택
  restore.py       # 새 프로세스 복원·결과 대조
  data/
  expected/        # 실제 정답 실행의 비교 결과
  outputs/         # 본인의 생성 결과
  reports/architecture_comparison.md
```

```powershell
python main.py
python restore.py
```

분류 RNN746·LSTM842·Transformer1162개 파라미터로 비슷한 범위지만 동일하지 않다. dropout0, 1층, 동일 분할·epoch·lr로 비교하며 모델 초기화는 같은 seed로 통제한다. 서로 다른 구조의 초기 가중치 자체가 같다는 뜻은 아니다. 예측 모델은 가변 길이6~12를 PackedSequence로 처리한다. loss 표에서 분류 Cross Entropy와 예측·재구성 MSE를 평균내지 않는다.

## main.py · 모듈형 시계열·재구성 프로젝트

PPT 87쪽과 연결한다. 이 프로젝트 폴더에서 실행한다.

```powershell
python main.py
```

### 직접 완성할 부분

- **D08**: 제공된 fit으로 LSTM 예측 모델을 학습하고 best 결과를 받는다.
- **D09**: Autoencoder를 입력 재구성 문제로 학습한다. forecast y와 섞지 않는다.

### 실행 결과 확인

아래 값 중 시간·처리량은 검수 PC의 관측 예시이다. **정답 숫자로 맞추지 않는다.** 같은 모델·데이터라도 실행 부하로 달라진다.

```text
task  params  best_epoch  valid_loss  valid_accuracy
      forecast     361          30    0.003160             NaN
reconstruction      42          40    0.176410             NaN
           RNN     746          25    0.001468             1.0
          LSTM     842          25    0.043251             1.0
   Transformer    1162          25    0.028943             1.0
test 구간/ID: 모델에 전달하지 않음
```

생성 파일: `outputs/architecture_comparison.csv`, `outputs/history.csv`, `outputs/predictions.csv`, `outputs/reconstruction.csv`, `outputs/classification_predictions.csv`, `outputs/mask_or_latent.png`

**완료 기준**: 과제별 표를 분리하고 손실 종류·best model·오류·한계를 보고한다.

### 자신의 말로 설명하기

- best epoch를 train과 valid 중 어디에서 골랐나? → 답: ____________________
- test를 사용한 곳이 있는가? → 답: ____________________
- 다음 값 예측과 재구성 모델의 오류 사례·한계를 구분했나? → 답: ____________________

## restore.py · 새 프로세스 모델 복원

PPT 87쪽과 연결한다. 이 프로젝트 폴더에서 실행한다.

```powershell
python restore.py
```

### 직접 완성할 부분

- **D10**: 새로 만든 동일 구조 모델에 저장한 state_dict를 복원한다. 힌트: 본인이 생성한 신뢰하는 파일만 weights_only=True로 읽는다.

### 실행 결과 확인

```text
model  ids_equal  values_equal
      forecast       True          True
reconstruction       True          True
           RNN       True          True
          LSTM       True          True
   Transformer       True          True
```

생성 파일: `outputs/restore_check.csv`

**완료 기준**: main 실행 후 별도 프로세스 restore로 ID·예측·오류를 대조한다.

### 자신의 말로 설명하기

- best epoch를 train과 valid 중 어디에서 골랐나? → 답: ____________________
- test를 사용한 곳이 있는가? → 답: ____________________
- 다음 값 예측과 재구성 모델의 오류 사례·한계를 구분했나? → 답: ____________________


`restore.py`는 모델을 다시 학습하지 않는다. 저장한 구조로 새 모델을 만든 뒤 가중치를 읽고 valid ID·예측·MSE를 대조한다. 외부의 알 수 없는 checkpoint를 읽지 않는다.

## 최신 수정판 · D11~D12

프로젝트의 `tests/test_contracts.py`에서 평가 상태 보존과 Padding 값 변경 불변성을 검사합니다. 기존 10곳에 2곳을 추가하여 심화는 12개 구현 항목입니다. 프로젝트 폴더에서 `python -m unittest discover -s tests -v`를 실행하세요. 수강생용 `self.fail`은 미완성 표시이므로 검사 없이 지우지 않습니다. `evaluate()`의 원래 모드 복구 코드는 제공했습니다.
