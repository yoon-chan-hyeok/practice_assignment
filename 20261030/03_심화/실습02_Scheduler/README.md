# Scheduler · 심화

PPT 26쪽 대응. `main.py` 한 파일에서 실험합니다.

입력 `data/points.csv`, 생성 `outputs/`, 비교 `expected/`입니다. 이 폴더만 따로 복사해도 실행할 수 있습니다.

## 구현할 부분

### S02
현재 epoch의 valid_loss를 scheduler.step(valid_loss)에 전달하세요.
optimizer.step은 batch마다, Plateau scheduler.step은 valid 계산 뒤 epoch마다 1번입니다.
lr_used는 이번 epoch, lr_next는 다음 epoch에 사용할 값입니다.

## 실행
```console
python main.py
```

## 실제 정답 실행 예
```text
fixed best epoch: 58 best valid loss: 0.011199 iterations: 8 lr 감소 epoch: []
plateau best epoch: 35 best valid loss: 0.022345 iterations: 8 lr 감소 epoch: [20, 36, 39, 42, 45, 48, 51, 54, 57, 60]
시간은 experiment_table.csv에 기록하며 CPU/GPU·실행 부하에 따라 달라집니다.
```

`expected/experiment_table.csv`와 각 `history_*.csv`, `curves_*.png`를 함께 대조하세요. 실행 시간은 환경에 따라 다르므로 일치 기준에서 제외합니다.

## 반드시 설명할 것
바꾼 조건, 고정 조건, best/last 결과와 해석의 한계를 기록하세요.

- best epoch와 마지막 epoch를 구분했나요?
- 같은 epoch의 갱신 횟수도 같았나요?
- 스케줄러는 valid 평가 뒤 호출했나요?
- test를 사용하지 않았나요?

내 기록: ________________________
## 오늘의 공통 실험 규칙
- **test는 오늘도 보관합니다.** 모형 선택·Early Stopping·학습률 조정에는 train/valid만 사용합니다.
- 후보마다 모델·Optimizer를 새로 만들고 seed를 재설정합니다. 앞 후보의 학습을 이어받지 않습니다.
- mini-batch 비교에서는 shuffle Generator도 같은 seed로 새로 만듭니다. 데이터 순서는 Dropout의 난수와 분리합니다.
- `train_loss_step`은 학습 도중 각 배치에서 측정한 손실입니다. 곡선의 `train_loss_eval`과 `valid_loss`는 **epoch 종료 후 같은 모델을 eval 모드로** 측정합니다.
- 후보·seed·epoch·batch size를 사전에 기록하고, 좋지 않은 결과도 그대로 남깁니다. ‘개선 후보’가 반드시 개선되어야 하는 과제가 아닙니다.
- 같은 epoch 수가 같은 optimizer 갱신 횟수는 아닙니다. 배치 실험에서는 iterations/total_steps도 확인합니다.
- 반복 seed 편차는 이 작은 실험의 변동입니다. 일반적인 알고리즘 순위나 통계적 유의성을 주장하지 않습니다.
- 모든 수치는 작은 합성 자료의 교육용 결과입니다. 실서비스 성능·GPU 속도 우위를 의미하지 않습니다.

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
