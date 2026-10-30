# 실습07~08 · 모듈형 ANN 프로젝트

PPT의 `day9_ann` 구조를 사용합니다. 정상200건 중 train120·valid40만 모델에 전달합니다. 2→8→2 ANN, CrossEntropyLoss, SGD(lr=0.1), batch32, 80epoch를 고정합니다.

```text
day9_ann/
  main.py              # 전체 실행
  model.py             # 제공된 ANN 클래스
  train.py             # 한 epoch 학습 / 평가
  check_gpu.py         # 장치 선택·기록
  restore.py           # 실습08 복원
  data/points.csv
  outputs/
  expected/
  reports/learning_note.md
```

## 구현 순서

1. `train.py` H07: gradient 계산·파라미터 갱신.
2. `train.py` H08: 평가 logits의 클래스 선택. 평가에는 backward가 없습니다.
3. `main.py` H09: 파라미터 사전 저장.
4. `restore.py` H10: 자신이 생성한 파라미터 사전 복원.

```powershell
python main.py
python restore.py
```

새 터미널에서 restore.py를 실행하여 별도 프로세스로 확인합니다. `map_location="cpu"`와 `weights_only=True`를 명시합니다. 학습한 전체 Python 객체를 저장하지 않으며, 신뢰하지 않는 외부 모델 파일을 로드하지 않습니다.

## 결과

- `gpu_check.txt`: 실제 환경·장치.
- `training_history.csv`: epoch1~80, train_loss_online, valid_loss, valid_accuracy.
- `final_metrics.json`: 표본 수·장치·손실·정확도·test 미사용.
- `validation_predictions.csv`: valid ID·실제값·예측.
- `model_state.pt`: 직접 실행하여 생성. 배포 ZIP에는 없음.

`train_loss_online`은 학습 중 각 batch의 평균 loss×행 수를 합산한 뒤120으로 나눈 값입니다. 매 batch 갱신되므로 학습 종료 후 train 전체를 한번에 평가한 값과는 다를 수 있습니다. 평가에서 `.eval()`과 `no_grad()`를 구분합니다.

## 실제 CPU 실행 결과

```text
10 0.342276 0.281476 0.975
20 0.234005 0.182579 0.975
30 0.180513 0.134341 1.0
40 0.147421 0.105641 1.0
50 0.126812 0.086818 1.0
60 0.111919 0.074174 1.0
70 0.09961 0.064484 1.0
80 0.090861 0.057217 1.0
저장 완료. 다음 순서: python restore.py
ID 순서 동일: True
예측 동일: True
서로 다른 CPU/GPU의 마지막 비트까지 동일함을 보장하는 검사는 아닙니다.
```

`reports/learning_note.md`에 역할 분리·손실 집계·평가 모드·복원 결과를 적습니다. GPU 환경에서는 CPU로 복원한 확률의 마지막 비트가 다를 수 있으며, 동일 seed만으로 다른 장치의 완전 동일성을 보장하지 않습니다. 기본필수와 달리 200건이므로 수치를 섞어 비교하지 마세요.


### v2 실습08 · 직접 작성하는 두 테스트
`tests/test_training.py`의 H11·H12를 완성하고 `python -m unittest discover -s tests -v`를 실행합니다. 제공된 정상 입력으로 마지막 배치 가중 평균과 평가의 비학습성을 확인합니다. 별도 모델 저장 파일 없이 테스트를 실행할 수 있습니다.
