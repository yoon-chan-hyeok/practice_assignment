# Day14 · 기본필수

**이 폴더의 README 하나로 01~08을 진행합니다.**

기본 결과는 소형 source Backbone 전이학습입니다. ImageNet ResNet18 성능이 아닙니다. 공식 ResNet18 경로는 최상위 README를 확인하세요.

## 파일 위치
Python 파일은 이 폴더에, 정상 입력은 `data/`에 있습니다. 결과는 이 폴더에 저장합니다.

VS Code로 이 폴더를 열고 터미널에서 아래 명령을 실행하세요. 파일의 위치를 기준으로 경로를 잡으므로 다른 작업 폴더에서도 절대 경로로 실행할 수 있습니다.

**TODO를 채우지 않은 코드는 실행돼도 정답이 아닙니다.** 출력·구현을 함께 확인하세요. 시험용 정상 입력만 사용하며 불량 파일 처리 과제는 없습니다.

## 공통 실험 약속
`train`만 학습에 사용하고, `valid`에서 epoch·후보를 비교합니다. test는 클래스 매핑·중복 감사 외에 모델 학습·추론·설명·임계값 선택에 사용하지 않습니다. valid는 자연적인 입력·분포를 유지하고 무작위 재추출하지 않습니다.
`head`: 새 Head만 학습합니다. `partial`: 마지막 Conv(상위 단계는 해당 BatchNorm affine 포함)+Head를 학습합니다. `requires_grad`와 BatchNorm의 running 통계는 별개이며 기본 정책은 BN 통계 고정입니다.
모든 작은 모델은 RGB float `[0,1]`, 32×32 입력입니다. ImageNet의 Resize256→CenterCrop224→Normalize 경로와 섞지 않습니다.
Grad-CAM은 선택한 logit에 대한 반응 지도이지 원인·정답·탐지 박스가 아닙니다. 입력 32×32 좌표의 열지도를 같은 좌표의 이미지에 합성합니다.
오답이 없으면 `오답 0건`이라고 쓰고 이미지를 억지로 만들지 않습니다. 05·06의 초기 모델과 07의 최종 모델 결과를 구분합니다. 낮은 성능도 정확히 실행·해석하면 정답입니다.


## 실습 01 · 데이터셋 구조·분할·불균형 · PPT 15쪽

열 파일: `01_dataset.py`. 직접 완성: B01

B01: ImageFolder로 train 폴더를 읽으세요. root는 필수 경로입니다.

```powershell
python 01_dataset.py
```

**사용 함수·인자**
`ImageFolder(root, transform=None)`: **root 필수**, 이미지 변환 transform은 선택. `.class_to_idx`는 클래스 이름→번호, `.targets`는 파일 순서와 같은 라벨 목록입니다. `.samples`를 보는 것은 학습이 아닙니다.

**확인 출력 — 제공 CPU 환경의 정답 실행**
```text
class_to_idx: {'circle': 0, 'square': 1, 'triangle': 2}
train 개수: [12, 6, 3] 같은 매핑: True
valid 개수: [3, 3, 3] 같은 매핑: True
test 개수: [2, 2, 2] 같은 매핑: True
```


**완료 기준**: TODO 구현, 위 수치·행 수·Shape와 대조, 생성 파일이 있다면 열어 확인.

**설명 질문**: 클래스 이름을 바꾸면 어떤 계약이 바뀌는가? train의 비율과 valid의 비율을 왜 따로 보는가?

내 설명: ______________________________


## 실습 02 · 사전학습 Backbone·새 Head · PPT 25쪽

열 파일: `02_head.py`. 직접 완성: B02

B02: 256개 특징에서 3개 logit을 출력하는 새 Linear Head를 만드세요.

```powershell
python 02_head.py
```

**사용 함수·인자**
`nn.Linear(in_features, out_features, bias=True)`: 입력·출력 수 **필수**, bias는 선택. `resnet18(*, weights=None, progress=True)`는 필수 위치 인자가 없으며 `weights`는 키워드 인자입니다. `np.load(file, allow_pickle=False)`는 배열 묶음을 읽는 제공 코드입니다. `.requires_grad`는 함수가 아니라 Parameter 속성입니다.

**확인 출력 — 제공 CPU 환경의 정답 실행**
```text
source 종류: 별도 합성 이미지로 사전학습한 TinyShapeCNN
학습 파라미터: 771
출력 shape: (2, 3)
ResNet18 구조 확인용 Head 파라미터: 1539
주의: 위 ResNet18은 구조만 확인했습니다. ImageNet 학습 결과가 아닙니다.
```


**완료 기준**: TODO 구현, 위 수치·행 수·Shape와 대조, 생성 파일이 있다면 열어 확인.

**설명 질문**: 고정 Backbone과 새 Head는 각각 무엇을 학습하는가? 공식 ResNet18과 소형 source의 출처는 같은가?

내 설명: ______________________________


## 실습 03 · Freeze·Partial Fine-tuning · PPT 35쪽

열 파일: `03_finetune.py`. 직접 완성: B03

B03: 두 전략에서 Head(9)를 열고, partial일 때 두 번째 Conv(4)도 여세요.

```powershell
python 03_finetune.py
```

**사용 함수·인자**
`AdamW(params, lr=..., weight_decay=...)`: **params 필수**, lr·weight_decay 선택. `zero_grad()`는 누적 기울기 초기화, `backward()`는 미분, `step()`은 실제 갱신입니다. `.eval()`은 gradient를 끄는 함수가 아닙니다.

**확인 출력 — 제공 CPU 환경의 정답 실행**
```text
strategy  trainable  valid_accuracy
    head        771             1.0
 partial       1923             1.0
```

숫자의 마지막 자릿수는 라이브러리·장치에 따라 달라질 수 있습니다. 시간은 정답으로 고정하지 않습니다.

**완료 기준**: TODO 구현, 위 수치·행 수·Shape와 대조, 생성 파일이 있다면 열어 확인.

**설명 질문**: requires_grad=False와 eval()은 어떤 점에서 다른가? partial은 어떤 층을 여는가?

내 설명: ______________________________


## 실습 04 · 클래스 불균형 대응 · PPT 47쪽

열 파일: `04_imbalance.py`. 직접 완성: B04

B04: f1_score에 average="macro", labels=[0,1,2], zero_division=0을 넣으세요.

```powershell
python 04_imbalance.py
```

**사용 함수·인자**
`f1_score(y_true, y_pred, average="macro", labels=[0,1,2], zero_division=0)`: 실제값·예측값 **필수**, 나머지는 선택 옵션. macro는 클래스별 F1의 동일 가중 평균입니다. `CrossEntropyLoss(weight=...)`는 train 손실에만 클래스 가중치를 적용합니다.

**확인 출력 — 제공 CPU 환경의 정답 실행**
```text
클래스 수: [12, 6, 3]
Accuracy: 0.5714
Macro F1: 0.2424
              precision    recall  f1-score   support

      circle      0.571     1.000     0.727        12
      square      0.000     0.000     0.000         6
    triangle      0.000     0.000     0.000         3

    accuracy                          0.571        21
   macro avg      0.190     0.333     0.242        21
weighted avg      0.327     0.571     0.416        21
```


**완료 기준**: TODO 구현, 위 수치·행 수·Shape와 대조, 생성 파일이 있다면 열어 확인.

**설명 질문**: Accuracy는 높고 minority Recall은 0일 수 있는가? weight와 sampler는 무엇을 각각 바꾸는가?

내 설명: ______________________________


## 실습 05 · 평가·오류 이미지 분석 · PPT 57쪽

열 파일: `05_errors.py`. 직접 완성: B05

B05: 실제 y_valid와 predictions로 혼동행렬을 만드세요. 행=실제, 열=예측.

```powershell
python 05_errors.py
```

**사용 함수·인자**
`confusion_matrix(y_true, y_pred, labels=[0,1,2])`: **실제값·예측값 필수**, labels는 선택이지만 이 수업에서는 순서 고정. 행=실제, 열=예측. `classification_report`의 target_names는 labels와 같은 순서입니다. 분모 0을 0으로 보고하는 정책을 명시합니다.

**확인 출력 — 제공 CPU 환경의 정답 실행**
```text
혼동행렬:
 [[3 0 0]
 [1 2 0]
 [3 0 0]]
              precision    recall  f1-score   support

      circle      0.429     1.000     0.600         3
      square      1.000     0.667     0.800         3
    triangle      0.000     0.000     0.000         3

    accuracy                          0.556         9
   macro avg      0.476     0.556     0.467         9
weighted avg      0.476     0.556     0.467         9

오답 개수: 4
square_002.png 실제: square 예측: circle
triangle_000.png 실제: triangle 예측: circle
triangle_001.png 실제: triangle 예측: circle
```


**완료 기준**: TODO 구현, 위 수치·행 수·Shape와 대조, 생성 파일이 있다면 열어 확인.

**설명 질문**: 오답 이미지 하나의 실제·예측·확률을 근거로 관찰과 가설을 나누어 적어라. 오답이 없을 때는 어떻게 보고하는가?

내 설명: ______________________________


## 실습 06 · Grad-CAM·편향 가설 · PPT 68쪽

열 파일: `06_gradcam.py`. 직접 완성: B06

B06: 채널 가중합에 relu()를 적용해 양의 반응만 남기세요.

```powershell
python 06_gradcam.py
```

**사용 함수·인자**
`torch.autograd.grad(outputs, inputs)`: 미분할 scalar·대상 Tensor **필수**. 입력을 수정하지 않고 gradient tuple을 반환합니다. `.mean(dim=(2,3), keepdim=True)`는 공간 평균. `cv2.addWeighted(src1, alpha, src2, beta, gamma)`는 앞의 다섯 인자 **필수**, 같은 좌표·크기의 BGR 이미지끼리 합성합니다.

**확인 출력 — 제공 CPU 환경의 정답 실행**
```text
correct circle_000.png target: circle CAM: (32, 32)
wrong square_002.png target: circle CAM: (32, 32)
```


**완료 기준**: TODO 구현, 위 수치·행 수·Shape와 대조, 생성 파일이 있다면 열어 확인.

**설명 질문**: Heatmap의 target은 무엇인가? 같은 이미지에서 target이 바뀌면 지도가 달라질 수 있는가?

내 설명: ______________________________


## 실습 07 · 전이학습 프로젝트 · PPT 78쪽

열 파일: `07_project.py`. 직접 완성: B07, B08, B09

B07: 역전파와 Optimizer 갱신을 수행하세요.
B08: 각 행의 가장 큰 logit 열을 예측 라벨로 고르세요.
B09: metrics를 UTF-8 JSON 문자열로 저장하세요. 아래 제공된 경로를 사용합니다.

```powershell
python 07_project.py
```

**사용 함수·인자**
`DataFrame.to_csv(path, index=False)`: 여기서는 출력 경로를 명시합니다. `torch.save(obj, path)`는 **저장 객체·경로 필수**. 복원할 때는 본인이 생성한 파일에만 `torch.load(..., weights_only=True)`를 사용합니다. 기본필수는 모델 파일 저장을 요구하지 않습니다.

**확인 출력 — 제공 CPU 환경의 정답 실행**
```text
{"accuracy": 1.0, "best_epoch": 8, "macro_f1": 1.0, "source": "synthetic_source_pretraining", "test_used": false, "valid_n": 9}
오답 수: 0 예측 행: 9 test 사용: False
```

숫자의 마지막 자릿수는 라이브러리·장치에 따라 달라질 수 있습니다. 시간은 정답으로 고정하지 않습니다.

**완료 기준**: TODO 구현, 위 수치·행 수·Shape와 대조, 생성 파일이 있다면 열어 확인.

**설명 질문**: 어떤 입력·설정·seed·매핑을 고정해야 재실행 결과를 비교할 수 있는가? test를 왜 남겨 두는가?

내 설명: ______________________________


## 실습 08 · 같은 프로젝트 재현 (PPT 83쪽)
07번 파일을 다시 실행합니다. 원본 data가 바뀌지 않았는지, metrics·predictions의 행 순서·값이 같은지 확인합니다.
최종 모델에 오답이 없으면 05·06의 초기 모델 오류와 분리하여 보고합니다. 마지막에 없는 오류를 만들거나 라벨을 바꾸지 않습니다.

| 기록 | 직접 작성 |
|---|---|
| 사용 모델·source 출처 | |
| train/valid 클래스 개수 | |
| 학습 범위·BN 정책 | |
| 주 지표와 이유 | |
| 관찰한 오류·CAM target | |
| 재실행 확인·한계 1개 | |

**07 생성 파일**: `metrics.csv`, `predictions.csv`, `history.csv`, `confusion.csv`, `project_cam.png`, 실제 오답이 있으면 `project_error_*.png`. 기본필수는 `metrics.json`도 생성합니다. 응용의 비교표는 세 후보를 포함하며 `predictions.csv`는 마지막 head+weight 후보의 예측입니다.
**06 생성 파일**: 기본 `cam_correct.png`·`cam_wrong.png`(해당 사례가 있을 때), 응용 `target_0_cam.png`·`target_1_cam.png`.

## 자주 막히는 지점
- 파일을 못 찾는 경우: ZIP 안에서 실행하지 말고 전체 압축을 푼 뒤 실행합니다. data를 삭제하지 않습니다.
- 같은 파일이 실행되는데 출력이 다른 경우: TODO, seed, source 배열, split, mode를 순서대로 확인합니다.
- Grad-CAM이 전부 0인 경우: 그 target의 양의 가중 반응이 없을 수 있습니다. 무조건 예쁜 열지도로 바꾸지 않습니다.
- `eval()` 안에서도 미분은 가능하지만 `inference_mode()`에서는 Grad-CAM을 계산하지 않습니다.
- 공식 ResNet18을 실행할 때는 Weight 사전 준비가 별도 필요합니다. 소형 source 실습은 다운로드 없이 진행합니다.

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

## 공식 참고자료
- [Torchvision ResNet18: Weight와 transforms](https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.resnet18.html)
- [PyTorch 전이학습 튜토리얼](https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)
- [CrossEntropyLoss: 가중 평균의 분모](https://docs.pytorch.org/docs/2.10/generated/torch.nn.CrossEntropyLoss.html)
- [DataLoader·WeightedRandomSampler](https://docs.pytorch.org/docs/2.10/data.html)
- [Module: train/eval·requires_grad·hook](https://docs.pytorch.org/docs/2.10/generated/torch.nn.Module.html)
- [classification_report](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html)
- [Grad-CAM 원 논문](https://arxiv.org/abs/1610.02391)
기술 문서의 최신 버전 표기와 아래 실제 검증 환경을 혼동하지 않습니다.
