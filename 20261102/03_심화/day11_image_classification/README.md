# 모듈형 최종 프로젝트 · day11_image_classification

## 파일의 책임

| 파일/폴더 | 역할 |
|---|---|
| `data.py` | ImageFolder·train/valid transform·DataLoader |
| `models.py` | SmallCNN·ResNet18·동결/BN 모드 |
| `train.py` | 표본 수 가중 학습·평가·계측 |
| `main.py` | 학습·best 선택·결과표·오류 이미지·checkpoint |
| `restore.py` | 모델 복원·ID/클래스/확률/예측 대조 |
| `data/` | 고정 PNG와 manifest. test는 보관 |
| `outputs/` | 직접 생성한 결과 |
| `expected/` | 실제 CPU small 모델의 참고 결과 |
| `reports/model_comparison.md` | 자신의 판단과 한계 |

## 직접 구현

**D08**: train.py의 backward → step. **D09**: main.py에서 최소 valid loss 상태를 deepcopy. **D10**: restore.py에서 state_dict 복원.
단순히 마지막 epoch의 파라미터를 저장하지 않습니다. 딕셔너리 참조만 저장하면 후속 학습에 따라 best 상태도 바뀔 수 있습니다.

## 실행

```powershell
python main.py --models small --epochs 3
python restore.py --name small
```

실제 사전학습 가중치를 준비한 뒤 세 경로를 한 실행으로 비교합니다. CPU에서는 작업량이 더 많습니다.

```powershell
python main.py --models small head partial --epochs 3
python restore.py --name head
```

`restore.py`는 **다운로드하지 않고** 저장된 실제 가중치를 구조에 적재합니다. `pretrained=False`로 구조만 만든 뒤 checkpoint를 읽는 것은 무작위 가중치 전이 실험과 다릅니다.

## 결과와 완료 기준

`model_comparison.csv`, `history_*.csv`, `predictions_*.csv`, `confusion_*.csv`, `curve_*.png`, `errors_*/`, `best_*.pt`를 생성합니다. 오분류가 0건이면 `errors_*/README.txt`에 0건을 기록합니다. 이미지를 만들어 오류를 꾸미지 않습니다.
`restore_report.json`의 same_ids·same_classes·same_predictions·same_probability가 True인지 확인합니다. GPU 학습과 CPU 복원에는 부동소수점 오차를 허용합니다. 가까운 경계 샘플의 클래스가 달라지면 숨기지 말고 보고합니다.
학습 시간은 전체 epoch train+eval을 포함하고 다운로드·모델 구성은 제외합니다. 07의 한 epoch 학습-only 시간과 같은 수치가 아닙니다.

`expected/`는 small 모델만 실제 학습한 결과입니다. 실제 pretrained Head/Partial 결과는 다운로드 제한으로 미검증입니다. 보고서에는 미실행/미측정을 0으로 채우지 않습니다.

## v2 추가 테스트 · D11/D12
`tests/test_project.py`의 두 구현 항목을 작성합니다. 테스트 입력·모델 생성 코드는 제공되어 있습니다.
`python -m unittest discover -s tests -v`로 실행하고, 미완성 상태는 통과로 처리하지 않습니다.
평가 함수는 표본 수로 가중한 CE와 정확도를 계산하고 호출 전 혼합 train/eval 상태를 복구합니다.
checkpoint 복원은 동일 구조·클래스 순서·전처리에서 확인합니다. `expected/`를 읽어 결과를 반환하면 안 됩니다.
