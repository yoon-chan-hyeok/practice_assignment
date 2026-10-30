# 실습07~08 · day10_stability

**먼저 `train.py`의 S07·S08, `experiments.py`의 S09를 완성하고 실행합니다. 다음 `restore.py`의 S10으로 복원합니다.**

```text
day10_stability/
  data.py          # 고정 train/valid를 읽기: 제공
  model.py         # 후보의 ANN 구조: 제공
  evaluate.py      # mode·no_grad를 적용한 평가: 제공
  train.py         # 학습·Scheduler·Early Stopping: S07, S08
  experiments.py   # 4후보 비교와 저장: S09
  restore.py       # 새 프로세스 복원: S10
  data/points.csv
  outputs/         # 실행한 CSV·PNG·JSON
  checkpoints/     # 직접 생성하는 best_model.pt
  expected/        # 정답 실행 비교 자료; 학습된 모델 없음
  reports/stability_report.md
```

## 실행 순서
```console
python experiments.py
python restore.py
```
두 번째 명령은 첫 번째가 생성한 best_config.json·best_model.pt·validation_predictions.csv를 사용합니다.
자신이 직접 생성한 체크포인트만 읽습니다. 공개된 출처 불명 .pt는 읽지 않습니다.

## 실험 조건
train240/valid80, width32, batch32, seed42. baseline과 Dropout0.3·BatchNorm·WD0.01을 각각 비교합니다.
lr=0.01, 최대80 epochs, 공통 Plateau factor0.5/patience3, Early Stopping patience8/min_delta0.001입니다.
모든 후보에 같은 종료 정책을 적용하므로 **실제 수행 epoch는 다를 수 있습니다.** stop_epoch도 함께 보고합니다.
한 번에 하나의 규제를 바꾸며 best valid loss가 가장 작은 후보를 고릅니다. 동점은 설정 목록의 앞 후보를 유지합니다.

## best와 patience는 다른 기록
best_state는 관측한 최저 valid loss의 실제 모델입니다. `copy.deepcopy`로 독립 사본을 만듭니다.
patience 카운터는 reference보다 min_delta를 넘게 감소한 경우에만 초기화합니다.
따라서 아주 작은 개선은 best에 저장되지만 patience를 초기화하지 않을 수 있습니다.
마지막 epoch의 모델을 반환하는 대신 best_state를 복원하고, 복원 loss와 best 기록을 대조합니다.
`best_model.pt`는 추론용 state_dict입니다. Optimizer까지 복원하는 학습 재개는 특심화의 별도 과제입니다.

## 제출
experiment_table.csv, history_*.csv, best_config.json, learning_curves.png, validation_predictions.csv,
restore_report.json과 reports/stability_report.md를 제출합니다. test 평가 결과는 요구하지 않습니다.

### S07
배치 loss의 역전파 후 optimizer로 파라미터를 갱신하세요.
loss는 배치 평균입니다. 로그 집계에서는 loss.item()*배치건수를 누적해야 합니다.

### S08
관측한 valid loss가 더 작을 때 state_dict를 copy.deepcopy로 보관하세요.
단순 대입은 이후 학습에 따라 바뀌므로 best_state가 최적 epoch를 보존하지 못합니다.
이 best는 관측 최소값이고, patience 재설정용 min_delta 기준은 별도입니다.

### S09
선택한 모델의 state_dict를 checkpoints/best_model.pt에 저장하세요.
선택 config는 best_config.json에 이미 기록됩니다. 학습 재개용이 아닌 추론 복원용입니다.

### S10
직접 생성한 state_dict만 torch.load(..., map_location="cpu", weights_only=True)로 읽어 모델에 적용하세요.
복원한 모델을 eval로 바꾸는 것과 no_grad를 쓰는 것은 별개입니다. 그 아래 evaluate가 처리합니다.

## CPU 실행 예
```text
baseline best epoch: 40 stop: 43 best valid loss: 0.020061
dropout best epoch: 28 stop: 36 best valid loss: 0.035909
batchnorm best epoch: 21 stop: 29 best valid loss: 0.035851
weight_decay best epoch: 46 stop: 51 best valid loss: 0.013377
선택: weight_decay / test 미사용 / validation 재사용에 따른 선택 편향 주의
```

```text
{
  "ids_equal": true,
  "predictions_equal": true,
  "valid_loss": 0.013376775197684765,
  "expected_loss": 0.0133767751976847,
  "loss_matches": true,
  "valid_accuracy": 1.0,
  "test_used": false
}
```
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


## v2 실습08 추가 구현 · S11/S12
`tests/test_training.py`의 검증문 두 곳을 작성합니다. 설정·모델·실패 시나리오의 fixture는 제공합니다. 실습07을 완성하지 않아도 평가 함수 테스트부터 진행할 수 있습니다.

- **S11**: 평가 호출 후 모든 Parameter/BN buffer·기존 gradient·하위 모드가 보존되고 반환 예측이 그래프를 갖지 않는지 검사합니다.
- **S12**: `.79/.78`처럼 min_delta 미만의 개선에도 실제 최소 모델이 저장·복원됨을 검증합니다. 요약 수치만 비교하지 말고 저장된 모델 Tensor를 대조합니다.

```powershell
python -m unittest discover -s tests -v
python experiments.py
python restore.py
```
총 12개 TODO(S01~S12)이며, 모델 선택·평가·저장 방식은 기존 심화 흐름을 유지합니다. 직접 테스트해야 할 책임만 조금 늘렸습니다. 실제 CUDA 또는 분산 학습은 필수 범위가 아닙니다.
