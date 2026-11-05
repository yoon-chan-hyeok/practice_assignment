# day14_vision · 전이학습 분류 프로젝트
실습 07~08을 이어서 진행합니다. main(D07~D09), restore(D10) 외의 모듈은 제공 코드입니다.

| 파일/폴더 | 역할 |
|---|---|
| models.py | 모델·동결 범위·BN 정책 |
| engine.py | 학습·평가·Best state |
| explain.py | 실제 오류 이미지·Grad-CAM |
| main.py | 후보 실험·선택·산출물 저장 |
| restore.py | 직접 저장한 모델의 새 프로세스 복원 |
| data/ | 정상 원본·source 배열·출처 |
| expected/ | 정답 실행의 비교용 파일 |
| outputs/ | 직접 실행하여 생성 |
| reports/model_card.md | 선택 이유·오류 가설·한계 |

```powershell
python main.py
python restore.py
```
주 지표 Macro F1 최대 → 동률이면 valid loss 최소 → 그래도 같으면 미리 정한 후보 순서. Best epoch는 각 후보의 valid loss 최소입니다.
Sampler와 Class weight는 별개 후보이며 동시에 적용하지 않습니다. 샘플러의 추출 클래스 수는 history에 기록됩니다. weighted loss의 train objective와 비가중 valid loss는 같은 척도라고 직접 비교하지 않습니다.

## 예상 출력
```text
accuracy  macro_f1  circle_recall  square_recall  triangle_recall   loss strategy balance  best_epoch  trainable  epochs           source
      1.0       1.0            1.0            1.0              1.0 0.0126     head    none           8        771       8 synthetic_source
      1.0       1.0            1.0            1.0              1.0 0.0081  partial    none           8       1955       8 synthetic_source
      1.0       1.0            1.0            1.0              1.0 0.0066     head  weight           8        771       8 synthetic_source
      1.0       1.0            1.0            1.0              1.0 0.0065     head sampler           8        771       8 synthetic_source
선택: head sampler test 사용: False
```
복원은 ID 순서·확률·예측이 True여야 합니다. 시간 열은 비교 허용오차 대상이 아니라 측정값입니다.

## 결과
`metrics.csv`, `predictions.csv`, `metrics.json`, `history.csv`, `confusion.csv`, `cam_index.json`, `best_model.pt`, `cam_*.png`, 실제 오답이 있으면 `error_*.png`.
출처·target class는 cam_index에 기록합니다. 오답이 0이면 오류 분석은 실습05 초기 후보와 구분하여 제출합니다.

## 공식 ImageNet ResNet18 (선택·교실 사전 준비 필요)
```powershell
python resnet18_official.py --strategy head --epochs 2
python resnet18_official.py --strategy partial --epochs 2
```
실제 공식 가중치를 다운로드/캐시에서 읽습니다. 가중치 준비 전에는 실행하지 않습니다. 실패 시 무작위 Weight로 자동 대체하지 않습니다. 입력은 해당 Weight의 transforms(), 출력은 outputs/imagenet로 분리합니다. 본 제작 환경에서는 공식 가중치 다운로드가 차단되어 이 두 명령의 학습 성능은 미검증입니다. 소형 source와 수치를 한 비교표의 같은 조건으로 섞지 않습니다.

## 모델 출처와 PPT의 차이 — 먼저 읽기
**기본 실행 경로는 별도 합성 이미지로 실제 사전학습한 `TinyShapeCNN`입니다. ImageNet ResNet18이 아닙니다.**
외부 다운로드 실패 때문에 하루 실습이 멈추지 않도록 준비했습니다. `data/source_backbone.npz`에는 source train 240장으로 학습하고 source valid 60장으로 선택한 **Backbone의 수치 배열만** 있습니다. Target 데이터와 새 Head는 사전학습에 사용하지 않았습니다. `source_provenance.json`에 출처·seed·학습 조건·SHA256을 기록했습니다.
이 파일은 무작위 가중치를 전이학습이라고 이름 붙인 것이 아닙니다. `np.load(..., allow_pickle=False)`로 수치 배열을 읽습니다. 최종 Target 모델은 수강생이 직접 학습합니다. Source 모델 재생성 코드는 강사용 `운영/prepare_source.py`에 있습니다.
**PPT의 ResNet18 ImageNet 실습도 삭제하지 않았습니다.** `03_심화/day14_vision/resnet18_official.py`에 별도 실행 경로를 제공합니다. 공식 가중치가 없으면 다운로드하며, 실패 시 `weights=None`으로 자동 대체하지 않습니다. 현재 제작 환경에서는 공식 가중치 다운로드가 차단되어 실제 ImageNet 전이학습 성능은 미검증입니다.
02번 기본필수에서 `resnet18(weights=None)`를 사용하는 부분은 **구조·Head 파라미터 1,539개 확인 전용**입니다. 이를 사전학습 결과로 보고하지 않습니다.
PPT의 원본 합성 데이터·학습 상태는 PPT 파일에 없으므로, 배포 데이터의 실제 출력이 정답 기준입니다. PPT의 0.911·0.389 등 성능 수치를 맞추는 과제가 아닙니다.
## 공통 실험 약속
`train`만 학습에 사용하고, `valid`에서 epoch·후보를 비교합니다. test는 클래스 매핑·중복 감사 외에 모델 학습·추론·설명·임계값 선택에 사용하지 않습니다. valid는 자연적인 입력·분포를 유지하고 무작위 재추출하지 않습니다.
`head`: 새 Head만 학습합니다. `partial`: 마지막 Conv(상위 단계는 해당 BatchNorm affine 포함)+Head를 학습합니다. `requires_grad`와 BatchNorm의 running 통계는 별개이며 기본 정책은 BN 통계 고정입니다.
모든 작은 모델은 RGB float `[0,1]`, 32×32 입력입니다. ImageNet의 Resize256→CenterCrop224→Normalize 경로와 섞지 않습니다.
Grad-CAM은 선택한 logit에 대한 반응 지도이지 원인·정답·탐지 박스가 아닙니다. 입력 32×32 좌표의 열지도를 같은 좌표의 이미지에 합성합니다.
오답이 없으면 `오답 0건`이라고 쓰고 이미지를 억지로 만들지 않습니다. 05·06의 초기 모델과 07의 최종 모델 결과를 구분합니다. 낮은 성능도 정확히 실행·해석하면 정답입니다.

시간 seconds는 CPU 1-thread에서 학습 루프와 epoch별 valid 평가를 포함합니다. 마지막 오류 이미지/CAM 생성 시간은 제외합니다. 다른 장치·source·분할의 시간을 섞지 않습니다.
