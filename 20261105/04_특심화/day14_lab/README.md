# Day14 특심화 · 정확한 전이학습 실험
문법 강의는 최소화합니다. `contracts.py` 각 함수의 주석이 명세입니다. 제공된 호출부를 임의로 바꿔 검사를 통과시키지 않습니다.

## 핵심·선택
핵심: S02 학습 범위, S03 train 가중치, S04 가중 CE, S06 상태 보존 CAM, S08 정확한 학습, S09~S10 epoch 경계 저장·재개.
선택: S01 감사, S05 그룹 bootstrap, S07 Occlusion, stages 시연, CPU DDP/AMP. 하루에 모두 완성하는 것이 아니라 본인 주제를 선택합니다.

| ID | 함수 | 반드시 만족할 계약 |
|---|---|---|
| S01 | audit_manifest | 경로 안전·SHA256·지각 hash 후보·group leak. 원본 보존 |
| S02 | trainable_groups | 실제 Parameter·중복 없는 그룹·BN 모드·동결 목록 |
| S03 | imbalance_weights | train만 사용·빈 클래스 정책·표본별 sampler weights |
| S04 | weighted_ce | 분모 sum(w[y])·미분 연결·torch 참조와 동일 |
| S05 | group_bootstrap | group 단위 복원추출·중복 추출 반영·고정 라벨 |
| S06 | grad_cam | target logit·frozen backbone·원래 gradient/mode/buffer/RNG 보존 |
| S07 | occlusion_map | 같은 target·음수 감소량 보존·불완전 마지막 patch |
| S08 | train_epoch | AMP 순서·가중 분모의 전역 집계·배치 ID 기록 |
| S09 | save_checkpoint | 모델뿐 아니라 optimizer/scheduler/scaler/RNG/순서·원자적 교체 |
| S10 | load_checkpoint | 계약 먼저 확인·동일 실험 재개·새 프로세스 대조 |

## 독립 실행
```powershell
python -m unittest -v test_contracts.py
python main.py --mode audit
python main.py --mode stages
python main.py --mode cam
python main.py --mode bootstrap
python main.py --mode full
python main.py --mode part
python main.py --mode resume
```
출력은 `outputs/`. part는 2epoch, resume은 같은 설정으로 총 4epoch까지 이어집니다. full과 resume의 모델·optimizer·scheduler·scaler·history·배치 순서·난수 상태를 대조합니다. 조합의 기준은 CPU, 1 thread, num_workers=0, BN 통계 고정입니다. 임의 GPU/플랫폼에서 bitwise 일치를 보장하지 않습니다.

`cam`·`bootstrap`은 **고정된 초기 1epoch 진단 후보**를 사용합니다. 최종 후보의 성능으로 발표하지 않습니다. Bootstrap은 그룹 독립성·대표성을 가정하고 모델 선택 편향까지 제거하지 않습니다. 검은 패치 가림 역시 분포 밖 조작일 수 있습니다.

## 선택: CPU 분산 학습의 가중 평균 확인
```powershell
python ddp_demo.py
```
Gloo 2개 프로세스에서 가중 CE의 gradient를 단일 전체 batch와 비교합니다. DDP는 gradient를 world size로 평균하므로 로컬 가중 손실 분자의 스케일을 global denominator에 맞춥니다. 이것은 CPU 분산 수치 검사이지 다중 GPU 성능 검증이 아닙니다.

## 선택: CUDA AMP
```powershell
python main.py --mode full --amp
```
실제 CUDA 장치가 있을 때만 실행합니다. 기본 CPU 검수에서는 CUDA 테스트 2개가 skip이며 성공으로 세지 않습니다.

## 완료 기준
선택한 요구 ID·원시 결과·자동 검사 출력·실패 시 보존된 상태·한계를 보고합니다. hash·CAM·신뢰구간·한 번의 점수로 데이터의 진실성이나 모델의 인과적 설명을 증명하지 않습니다.
본인이 만든 체크포인트만 로드합니다. data/의 정상 입력은 변경하지 말고 경계/실패 테스트는 임시 폴더에서 만듭니다.

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
## 공식 참고자료
- [Torchvision ResNet18: Weight와 transforms](https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.resnet18.html)
- [PyTorch 전이학습 튜토리얼](https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)
- [CrossEntropyLoss: 가중 평균의 분모](https://docs.pytorch.org/docs/2.10/generated/torch.nn.CrossEntropyLoss.html)
- [DataLoader·WeightedRandomSampler](https://docs.pytorch.org/docs/2.10/data.html)
- [Module: train/eval·requires_grad·hook](https://docs.pytorch.org/docs/2.10/generated/torch.nn.Module.html)
- [classification_report](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html)
- [Grad-CAM 원 논문](https://arxiv.org/abs/1610.02391)
기술 문서의 최신 버전 표기와 아래 실제 검증 환경을 혼동하지 않습니다.
