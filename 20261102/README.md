# 2026-11-02(월) Day11 · CNN·이미지 분류·전이학습

수강생용 TODO 코드입니다. 기본필수는 01_기본필수/README.md부터 시작합니다.

| 경로 | 대상·구조 | 구현 항목 |
|---|---|---:|
| `01_기본필수` | 기존 코드·데이터·README 그대로, 코드 8개와 이미지용 data/ | 9곳 |
| `02_응용` | code + data/·outputs/, 클래스별 지표·실제 오답 저장 추가 | 10곳 |
| `03_심화` | 실습별 안내 + 모듈형 프로젝트 + 평가/복원 테스트 | 12곳 |
| `04_특심화` | **교시별 독립 특심화01~08**, 상세 요구사항·공개 테스트 | 8실습·18곳 |

총 8교시의 활동입니다. 01~07은 각각 해당 단원, 08은 앞의 기능을 연결하는 프로젝트입니다. 기본필수/응용은 제공된 코드에서 핵심 부분만 작성합니다. 같은 교시 주제에서 난이도를 선택합니다. 특심화도 01~08마다 독립된 시작 코드·산출물·테스트가 있으며 앞 과제 미완성이 다음 시작을 막지 않습니다.

## 실행 환경

기존 Day9·Day10의 가상환경에서 실행합니다. VS Code에서 이 자료를 **폴더 열기**로 연 뒤 해당 Python 인터프리터를 선택합니다.

```powershell
python -c "import torch, torchvision; print(torch.__version__, torchvision.__version__); print('CUDA:', torch.cuda.is_available())"
python -m pip install numpy pandas pillow matplotlib
```

이미 torch·torchvision이 정상 동작하면 재설치하지 않습니다. 설치가 필요한 경우 두 라이브러리의 호환 조합과 GPU 드라이버를 먼저 확인하고 공식 설치 선택기를 사용합니다: https://pytorch.org/get-started/locally/
이번 v2를 실제 검사한 환경은 **Python 3.13.5 / torch 2.10.0+cpu / torchvision 0.25.0+cpu / numpy 2.3.5 / pandas 2.2.3 / Pillow 12.3.0 / Matplotlib 3.10.8 / Linux**입니다. 강의표의 미래 버전명을 검증 환경으로 바꿔 쓰지 않았습니다.
CPU-only 신규 환경의 설치 예시는 다음과 같습니다. **이미 GPU용 PyTorch가 설치된 환경에 덮어쓰지 않습니다.**

```powershell
python -m pip install torch==2.10.0 torchvision==0.25.0 --index-url https://download.pytorch.org/whl/cpu
```

새 특심화 공개 테스트는 표준 `unittest`로 실행하므로 pytest가 필수는 아닙니다. GPU·Windows·macOS에서의 직접 실행 검증은 수행하지 못했습니다. GPU가 없으면 CPU 결과를 제출하고 GPU의 시간·VRAM은 `N/A`로 기록합니다.


## 실습 06 시작 전: 실제 사전학습 가중치 준비

`resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)`는 공식 ImageNet 사전학습 가중치를 사용합니다. 최초 약 45MB 다운로드와 다음 실행을 위한 캐시가 필요합니다. 수업 전에 교사가 준비하세요.

```powershell
python -c "from torchvision.models import resnet18, ResNet18_Weights; resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)"
python -c "import torch; print(torch.hub.get_dir())"
```

오프라인 PC에는 **공식 사이트에서 받은** `resnet18-f37072fd.pth`를 출력된 hub 폴더의 `checkpoints` 안에 복사합니다. 가중치 파일은 이 ZIP에 넣지 않았습니다. 교사용 `운영/prepare_weights.py`로 다운로드·해시·전처리를 점검할 수 있습니다.

**이번 제작 환경에서는 공식 가중치 다운로드가 차단되어 실제 사전학습 모델의 학습·성능을 실행 검증하지 못했습니다.** 전이학습 파일에 임의의 정확도를 예상값으로 넣지 않았습니다. 무작위 가중치로 수행한 테스트는 동결·파라미터 그룹·BN 상태의 구조 검사일 뿐 전이학습 성능 검증이 아닙니다.

`weights=None`으로 바꿔 실행한 결과를 전이학습 결과로 제출하지 않습니다. 가중치를 준비하지 못했다면 해당 실습은 **미실행**으로 기록하고 교사 시연으로 동결 범위·파라미터 수를 확인합니다. 다른 실습은 독립적으로 진행할 수 있습니다.


## 학습 원칙

네 단계는 모두 풀어야 하는 숙제가 아닙니다. 기본필수에서 직접 코드를 바꾸고 설명할 수 있게 된 뒤 응용·심화·특심화를 선택합니다. 실행이 끝난 것만으로 완료가 아닙니다. TODO에 요구한 계산이 실제로 적용되었는지와 출력·설명을 함께 확인합니다.

기본필수는 사용자 정의 함수·클래스·예외처리 없이 제공합니다. 응용은 짧은 한 파일 실습과 `data/`, `outputs/`만 사용합니다. 심화는 체계적인 폴더를 사용하며 이번 v2에서 평가·복원 검증 두 항목을 조금 강화했습니다. 특심화는 함수 문법보다 소스의 **요구사항 주석**을 먼저 읽습니다.

이번 `ImageFolder` 학습에는 이미지용 클래스 폴더가 필요합니다. 이것은 기본필수에 코드 모듈을 늘리는 것이 아니라, 이미지와 정답의 관계를 보여 주는 최소 저장 구조입니다. 이미지를 직접 옮기거나 폴더 이름을 바꾸지 않습니다.

### 데이터

`horizontal=0`(가로 줄무늬), `vertical=1`(세로 줄무늬) 두 클래스의 RGB 64×64 정상 PNG입니다. 파일을 읽고 클래스 매핑을 직접 확인하세요. 본 자료용으로 로컬 생성한 합성 이미지이며 실제 사진의 성능을 대표하지 않습니다. 생성 seed는 110200을 기준으로 split·class·번호별로 독립 설정했습니다. 증강한 동일 원본이 서로 다른 분할에 들어가지 않습니다.

| 단계 | train | valid | test(보관) | 전체 |
|---|---:|---:|---:|---:|
| 기본필수 | 12 | 4 | 4 | 20 |
| 응용·심화 | 60 | 20 | 20 | 100 |
| 이미지 사용 특심화 폴더 | 60 | 20 | 미포함 | 80 |

각 분할은 두 클래스 수가 같습니다. 기본필수는 큰 데이터의 같은 split에서 일부를 사용합니다. **어느 단계도 test를 학습·선택·추론에 사용하지 않습니다.** 이번 과제는 최종 블라인드 성능을 보장하는 시험이 아니라 구현·비교 연습입니다.

가로·세로 클래스에는 좌우반전과 작은 밝기 변화가 적합하지만 **90도 회전은 라벨을 뒤집으므로 제외**합니다. 무작위 변환은 train에만, valid에는 결정적 변환만 사용합니다.

SmallCNN은 주로 32×32·ToTensor, ResNet18은 공식 가중치 변환(224×224·ImageNet Normalize)을 사용합니다. 두 모델의 입력 크기·학습률·배치·학습 범위가 다르면 차이를 결과표에 적고 순수한 구조 효과라고 단정하지 않습니다.

### 생성 파일과 재현

가중치·checkpoint는 미리 배포하지 않습니다. 실행하면 `.pt` 파일이 생깁니다. 직접 생성한 신뢰하는 파일만 `weights_only=True`로 읽습니다. `expected/`는 비교용 실제 실행 결과, `outputs/`는 본인의 실행 결과입니다. 시간·처리량 값은 PC마다 달라지므로 정답 숫자로 맞추지 않습니다. 같은 버전의 CPU 환경에서는 소수 오차를 허용하며 큰 차이는 seed·입력 크기·train/eval·weights를 확인합니다.


공식 문서(재확인일: 2026-10-28):
- ImageFolder: https://docs.pytorch.org/vision/stable/generated/torchvision.datasets.ImageFolder.html
- Conv2d: https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html
- ResNet18·가중치·전처리: https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.resnet18.html
- 전이학습: https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html
- AMP·기울기 누적: https://docs.pytorch.org/docs/stable/notes/amp_examples.html
- 메모리 형식: https://docs.pytorch.org/tutorials/intermediate/memory_format_tutorial.html
- 재현성: https://docs.pytorch.org/docs/stable/notes/randomness.html


## 최신 수정판의 실행 순서
기본필수의 학습 난이도·소스·입력은 그대로입니다. 응용은 A09(클래스별 지표), A10(실제 오답 저장), 심화는 D11/D12(평가·복원 테스트)를 추가했습니다. 특심화는 한 프로젝트 안의 여러 TODO가 아니라 **각 교시 폴더의 tasks.py/run.py/tests**로 분리했습니다.

**실제 ImageNet 전이학습은 별도 가중치 준비가 필요합니다.** 설치된 환경에 캐시가 없다면 교사가 준비한 뒤 06번을 실행합니다. 모델 준비가 안 되어도 다른 기본 실습과 종합 SmallCNN 프로젝트는 독립적으로 실행합니다. 무작위 가중치로 자동 대체하지 않습니다. 기본필수 파일 안의 미완성 `pass`는 프로그램 종료 여부가 아니라 README의 결과·코드를 함께 보고 평가합니다.

실습은 VS Code의 선택 가상환경에서 실행합니다. CUDA 버전을 임의로 새로 설치하지 마세요. 여러 프로그램을 동시에 학습시키지 말고 하나씩 실행합니다. 다운로드·시간 측정·실제 모델의 성능 수치는 미실행을 0으로 채우지 않습니다.
