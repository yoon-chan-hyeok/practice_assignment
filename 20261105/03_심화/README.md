# Day14 · 심화
코드 난이도는 예전 응용 수준입니다. 폴더는 역할별로 나눕니다.
실습01~06의 main.py는 제공된 day14_vision 모듈을 가져옵니다. 실습 폴더만 따로 복사하지 말고 03_심화 전체를 유지하세요.
프로젝트 day14_vision은 data도 자체 포함하므로 단독 복사 실행이 가능합니다.

1. 실습01_그룹분할: 이미지 분할과 그룹 분할 비교
2. 실습02_BN정책: 가중치 동결과 running 통계 동결 구분
3. 실습03_단계적해제: 처음부터 Partial vs Head→Partial
4. 실습04_불균형: 기준선·Class weight·Sampler 별도 비교
5. 실습05_오류가설: 초기 1epoch 모델의 실제 오류 분석
6. 실습06_GradCAM: 같은 target에 대한 원본·가림 비교
7. day14_vision/main.py: 비교·선택·저장
8. day14_vision/restore.py: 새 프로세스 복원

함수와 재사용 코드는 제공되어 있습니다. 총 TODO 10곳을 완성합니다. expected는 비교용, outputs는 직접 생성 결과, reports는 본인 해석입니다.

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
