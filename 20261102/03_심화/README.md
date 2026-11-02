# 심화 · 역할을 나눈 이미지 분류 프로젝트

코드 난이도는 이전 자료의 응용 수준을 유지합니다. 복잡한 오류 처리나 테스트 작성은 요구하지 않습니다. 실습별 폴더에서 README를 읽고 `main.py`를 실행합니다. 공통 이미지와 제공된 모델은 `day11_image_classification/`에 한 번만 두어 데이터 복제와 경로 혼동을 줄였습니다.

**개별 실습 폴더만 떼어 복사하지 말고 03_심화 전체를 이동하세요.** 종합 프로젝트 `day11_image_classification/`는 입력과 모듈이 함께 있어 단독 복사가 가능합니다.

| 순서 | 폴더 | 주제 |
|---|---|---|
| 01 | 실습01_파라미터 | MLP·Conv 파라미터 수 |
| 02 | 실습02_커널채널 | 채널·커널 후보 |
| 03 | 실습03_BN_Dropout | train/eval·통계 |
| 04 | 실습04_증강 | 라벨 보존 |
| 05 | 실습05_CNN비교 | 폭 8·16 비교 |
| 06 | 실습06_전이비교 | 실제 pretrained 비교·환경 사전 준비 |
| 07 | 실습07_Batch시간 | 같은 조건의 Batch·장치 계측 |
| 08 | day11_image_classification | 통합·best 저장·새 프로세스 복원 |

앞 실습은 프로젝트 TODO에 의존하지 않도록 학습 경로를 제공합니다. TODO D01~D07은 개별 실습, D08~D10은 마지막 프로젝트입니다. `expected/`는 실제 CPU 실행으로 만든 참고 결과이며 시간은 정답이 아닙니다. 사전학습 모델의 결과표는 검증되지 않아 제공하지 않습니다.

## 실습 06 시작 전: 실제 사전학습 가중치 준비

`resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)`는 공식 ImageNet 사전학습 가중치를 사용합니다. 최초 약 45MB 다운로드와 다음 실행을 위한 캐시가 필요합니다. 수업 전에 교사가 준비하세요.

```powershell
python -c "from torchvision.models import resnet18, ResNet18_Weights; resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)"
python -c "import torch; print(torch.hub.get_dir())"
```

오프라인 PC에는 **공식 사이트에서 받은** `resnet18-f37072fd.pth`를 출력된 hub 폴더의 `checkpoints` 안에 복사합니다. 가중치 파일은 이 ZIP에 넣지 않았습니다. 교사용 `운영/prepare_weights.py`로 다운로드·해시·전처리를 점검할 수 있습니다.

**이번 제작 환경에서는 공식 가중치 다운로드가 차단되어 실제 사전학습 모델의 학습·성능을 실행 검증하지 못했습니다.** 전이학습 파일에 임의의 정확도를 예상값으로 넣지 않았습니다. 무작위 가중치로 수행한 테스트는 동결·파라미터 그룹·BN 상태의 구조 검사일 뿐 전이학습 성능 검증이 아닙니다.

`weights=None`으로 바꿔 실행한 결과를 전이학습 결과로 제출하지 않습니다. 가중치를 준비하지 못했다면 해당 실습은 **미실행**으로 기록하고 교사 시연으로 동결 범위·파라미터 수를 확인합니다. 다른 실습은 독립적으로 진행할 수 있습니다.

## v2 · D11/D12 검증 과제
종합 프로젝트 `day11_image_classification/tests/test_project.py`에서 공개 테스트 두 곳을 완성합니다.
D11은 마지막 작은 배치의 가중 평균과 평가 전후 BN·weight·기존 gradient·개별 모드를 검사합니다.
D12는 신뢰하는 자체 checkpoint를 저장하고 새 모델로 로드한 뒤 logits를 대조합니다.

```powershell
cd day11_image_classification
python -m unittest discover -s tests -v
python main.py
python restore.py
```
이 테스트는 사전학습 가중치 다운로드 없이 실행됩니다. 단순히 출력이 맞는지뿐 아니라 저장·복원이 실제로 이루어지는지 설명하세요.
