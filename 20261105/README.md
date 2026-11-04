# Day14 · 2026-11-05(목) 전이학습·오류 분석 — 수강생용

## 시작
기본필수 → 응용 → 심화 → 특심화는 **선택 경로**입니다. 네 단계를 하루에 모두 끝내지 않습니다.
- 처음 배우는 수강생: `01_기본필수/README.md`
- 응용: 코드 + `data/` + `outputs/`의 얕은 구조
- 심화: 실습별 폴더와 `day14_vision` 모듈형 프로젝트
- 특심화: `04_특심화/day14_lab/README.md`, `contracts.py`의 요구 주석

강사용은 완성 코드·설명 주석, 수강생용은 TODO입니다. 기본필수는 사용자 정의 함수·클래스·예외처리 과제를 추가하지 않았습니다.
실습 01~06은 독립 실행, 07~08은 같은 프로젝트를 이어서 사용합니다. 이미지 입력의 `data/분할/클래스`는 ImageFolder를 배우기 위한 최소 구조입니다.

## 모델 출처와 PPT의 차이 — 먼저 읽기
**기본 실행 경로는 별도 합성 이미지로 실제 사전학습한 `TinyShapeCNN`입니다. ImageNet ResNet18이 아닙니다.**
외부 다운로드 실패 때문에 하루 실습이 멈추지 않도록 준비했습니다. `data/source_backbone.npz`에는 source train 240장으로 학습하고 source valid 60장으로 선택한 **Backbone의 수치 배열만** 있습니다. Target 데이터와 새 Head는 사전학습에 사용하지 않았습니다. `source_provenance.json`에 출처·seed·학습 조건·SHA256을 기록했습니다.
이 파일은 무작위 가중치를 전이학습이라고 이름 붙인 것이 아닙니다. `np.load(..., allow_pickle=False)`로 수치 배열을 읽습니다. 최종 Target 모델은 수강생이 직접 학습합니다. Source 모델 재생성 코드는 강사용 `운영/prepare_source.py`에 있습니다.
**PPT의 ResNet18 ImageNet 실습도 삭제하지 않았습니다.** `03_심화/day14_vision/resnet18_official.py`에 별도 실행 경로를 제공합니다. 공식 가중치가 없으면 다운로드하며, 실패 시 `weights=None`으로 자동 대체하지 않습니다. 현재 제작 환경에서는 공식 가중치 다운로드가 차단되어 실제 ImageNet 전이학습 성능은 미검증입니다.
02번 기본필수에서 `resnet18(weights=None)`를 사용하는 부분은 **구조·Head 파라미터 1,539개 확인 전용**입니다. 이를 사전학습 결과로 보고하지 않습니다.
PPT의 원본 합성 데이터·학습 상태는 PPT 파일에 없으므로, 배포 데이터의 실제 출력이 정답 기준입니다. PPT의 0.911·0.389 등 성능 수치를 맞추는 과제가 아닙니다.

## 환경 준비
전날 쓰던 가상환경을 그대로 사용합니다. VS Code에서 현재 난이도 폴더를 **폴더 열기**로 엽니다.
```powershell
python -c "import torch, torchvision, cv2; print(torch.__version__, torchvision.__version__, cv2.__version__)"
```
필요한 패키지는 `torch`, `torchvision`, `numpy`, `pandas`, `scikit-learn`, `opencv-python`, `Pillow`입니다.
`torch`·`torchvision`은 [PyTorch 공식 설치 선택기](https://pytorch.org/get-started/locally/)의 서로 호환되는 조합을 설치합니다. GPU용 설치를 CPU판으로 임의 덮어쓰지 않습니다.
나머지가 없을 때만 다음을 실행합니다.
```powershell
python -m pip install numpy pandas scikit-learn opencv-python Pillow
```
`opencv-python`과 `opencv-python-headless`를 동시에 새로 설치하지 않습니다. 이미 정상 import되면 재설치하지 않습니다.
검증 환경: Python 3.13.5, torch 2.10.0+cpu, torchvision 0.25.0+cpu, numpy 2.3.5, pandas 2.2.3, sklearn 1.8.0, OpenCV 4.13.0, Pillow 12.3.0, Linux. Windows·macOS와 실제 GPU는 미검증입니다.

## 데이터
기본필수: train 12·6·3장, valid 3·3·3장, test 2·2·2장 = **36장**.
응용·심화·특심화: train 120·40·20장, valid 30·30·30장, test 10·10·10장 = **300장**.
순서는 circle·square·triangle입니다. 실제 자연 사진이 아니라 이 실습용으로 새로 만든 정상 RGB 도형 이미지입니다. 원본을 덮어쓰지 않습니다.

## 공통 실험 약속
`train`만 학습에 사용하고, `valid`에서 epoch·후보를 비교합니다. test는 클래스 매핑·중복 감사 외에 모델 학습·추론·설명·임계값 선택에 사용하지 않습니다. valid는 자연적인 입력·분포를 유지하고 무작위 재추출하지 않습니다.
`head`: 새 Head만 학습합니다. `partial`: 마지막 Conv(상위 단계는 해당 BatchNorm affine 포함)+Head를 학습합니다. `requires_grad`와 BatchNorm의 running 통계는 별개이며 기본 정책은 BN 통계 고정입니다.
모든 작은 모델은 RGB float `[0,1]`, 32×32 입력입니다. ImageNet의 Resize256→CenterCrop224→Normalize 경로와 섞지 않습니다.
Grad-CAM은 선택한 logit에 대한 반응 지도이지 원인·정답·탐지 박스가 아닙니다. 입력 32×32 좌표의 열지도를 같은 좌표의 이미지에 합성합니다.
오답이 없으면 `오답 0건`이라고 쓰고 이미지를 억지로 만들지 않습니다. 05·06의 초기 모델과 07의 최종 모델 결과를 구분합니다. 낮은 성능도 정확히 실행·해석하면 정답입니다.

## 하루 운영
1교시 데이터 감사 20분 / 2~7교시 각 25분 / 8교시 재현·설명 30분. 총 실습 200분입니다.
기본필수만으로 평가 기준을 충족할 수 있습니다. 특심화의 분산·AMP·설명 비교는 선택 확장이며 CPU 과제를 먼저 완성합니다.

## 제출
실행 코드, `metrics.csv`, `predictions.csv`, 설명 기록(기본·응용은 README 작성란), 실제 오류 사례·CAM, 재실행 증거를 제출합니다. 심화는 `reports/model_card.md`를 사용합니다.
Git 사용자는 코드·README·데이터 출처를 기록하고 가상환경·캐시·Target 모델 파일은 커밋하지 않습니다. 새로 만드는 npz는 수업에서 출처를 제공한 source 배열과 구분합니다.

## 공식 참고자료
- [Torchvision ResNet18: Weight와 transforms](https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.resnet18.html)
- [PyTorch 전이학습 튜토리얼](https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)
- [CrossEntropyLoss: 가중 평균의 분모](https://docs.pytorch.org/docs/2.10/generated/torch.nn.CrossEntropyLoss.html)
- [DataLoader·WeightedRandomSampler](https://docs.pytorch.org/docs/2.10/data.html)
- [Module: train/eval·requires_grad·hook](https://docs.pytorch.org/docs/2.10/generated/torch.nn.Module.html)
- [classification_report](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html)
- [Grad-CAM 원 논문](https://arxiv.org/abs/1610.02391)
기술 문서의 최신 버전 표기와 아래 실제 검증 환경을 혼동하지 않습니다.

