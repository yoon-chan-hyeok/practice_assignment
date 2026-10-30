# Day10 · 심화

**코드 난이도는 기존 응용 수준이며 구조만 역할별로 정리합니다.**

실습01~06은 각각 폴더를 열고 README의 main.py를 실행합니다. 필요한 데이터는 각 폴더에 들어 있습니다.
실습07~08은 `day10_stability/README.md`로 이어갑니다.

- [WeightDecay](실습01_WeightDecay/README.md)
- [Scheduler](실습02_Scheduler/README.md)
- [Batch비교](실습03_Batch비교/README.md)
- [과적합진단](실습04_과적합진단/README.md)
- [Dropout비교](실습05_Dropout비교/README.md)
- [BN과규제](실습06_BN과규제/README.md)

- [실습 07~08 통합 프로젝트](day10_stability/README.md)

## 준비와 실행
전날 PyTorch가 정상 실행된 가상환경을 그대로 사용합니다. 오늘은 재설치·CUDA 변경이 과제가 아닙니다.

1. ZIP을 새 폴더에 압축 해제합니다. 이전 자료에 덮어쓰지 않습니다.
2. VS Code에서 **자신의 난이도 폴더**를 열고, 전날 사용한 Python 인터프리터를 선택합니다.
3. 새 터미널에서 `python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"`로 확인합니다.
4. PyTorch가 이미 있으면 `python -m pip install pandas matplotlib`만 필요합니다. 기본 데이터 처리는 pandas, 그림은 Matplotlib입니다.
5. PyTorch가 없다면 강사와 [공식 설치 선택기](https://docs.pytorch.org/get-started/locally/)에서 OS/CPU/CUDA에 맞는 명령을 정합니다. 모든 코드는 CPU로 수행 가능합니다. `torchvision`은 오늘 사용하지 않습니다.

실제 검수: Python 3.13.5 / PyTorch 2.10.0+cpu / NumPy 2.3.5 / pandas 2.2.3 / Matplotlib 3.10.8 / Linux.
PPT에 적힌 PyTorch 2.14·CUDA 13 조합을 이 환경에서 검증한 것은 아닙니다. Windows·macOS·실제 NVIDIA GPU 실행은 미검증입니다.
PPT API 설명과 검수 환경의 버전을 구분하고, 정상인 GPU 환경을 CPU 패키지로 덮어쓰지 마세요.

모든 실행 명령은 해당 `.py`가 있는 폴더의 터미널 기준입니다. Windows는 `cd "경로"`, macOS/Linux도 `cd "경로"`를 사용할 수 있습니다.
`python` 명령이 없을 때는 기관 PC 설정에 따라 `py`(Windows) 또는 `python3`를 사용합니다.
파일은 `__file__` 위치를 기준으로 읽으므로 다른 작업 폴더에서도 절대 경로 실행이 가능합니다.

## 새 함수·클래스 빠른 사전
‘선택값’ 열은 **이 실습에서 명시하는 값**이며, 라이브러리의 모든 기본값 목록은 아닙니다.

| 호출 | 역할·반환 | 필수 인자 | 이번에 다룰 선택 인자 |
|---|---|---|---|
| `torch.optim.SGD(params, ...)` | gradient로 파라미터를 갱신할 Optimizer 생성 | `params`: 보통 `model.parameters()` | `lr`, `momentum`, `weight_decay` |
| `torch.optim.AdamW(params, ...)` | 적응적 갱신과 분리된 가중치 감쇠 | `params` | `lr`, `weight_decay`; 기본 decay는 0.01이므로 비교 실험에서 0을 명시 |
| `optimizer.zero_grad()` | 이전 gradient를 비움 | 없음 | `set_to_none=True`: gradient를 None으로 초기화 |
| `optimizer.step()` | 현재 `.grad`로 한 번 갱신 | 없음 | 일반 학습에서는 선택 `closure`를 사용하지 않음 |
| `TensorDataset(*tensors)` | 같은 첫 차원의 Tensor를 묶은 Dataset | 이 실습에서는 X, y 두 Tensor | 추가 Tensor를 넣으면 함께 배치화됨 |
| `DataLoader(dataset, ...)` | Dataset을 배치로 순회하는 객체 | `dataset` | `batch_size`, `shuffle`, `generator`, `num_workers=0`, `drop_last=False` |
| `nn.Dropout(p=0.5)` | train에서 일부 activation을 0으로, eval에서 그대로 전달 | 없음 | `p`: 제거 확률, `inplace=False` |
| `nn.BatchNorm1d(num_features, ...)` | 특성별 batch 통계와 running 통계 사용 | `num_features`: 앞 Linear 출력 열 수 | `momentum=0.1`, `eps=1e-5`, `affine=True`, `track_running_stats=True` |
| `model.train(mode=True)` | 모듈 모드 설정, self 반환 | 없음 | `mode`; `eval()`은 `train(False)`에 해당 |
| `torch.no_grad()` | 안쪽 계산의 gradient 기록을 끄는 문맥 | 없음 | 모드를 바꾸지는 않음 |
| `ReduceLROnPlateau(optimizer, ...)` | valid 지표가 개선되지 않을 때 lr 감소 | `optimizer` | `mode='min'`, `factor`, `patience`, `threshold`, `threshold_mode` |
| `scheduler.step(valid_loss)` | Plateau의 상태·lr 갱신 | Plateau는 `metrics` | 기본적으로 epoch 번호는 직접 전달하지 않음 |
| `CosineAnnealingLR(optimizer, T_max, ...)` | 미리 정한 cosine 일정으로 lr 변경 | `optimizer`, `T_max` | `eta_min`; `.step()`에 loss를 넣지 않음 |
| `copy.deepcopy(model.state_dict())` | best 시점 가중치·BN 버퍼의 독립 사본 | 복사할 객체 | 단순 대입으로 대체하면 값이 따라 바뀔 수 있음 |
| `torch.save(obj, path)` | 직접 만든 상태 저장 | `obj`, 저장 경로 | 전체 Module 대신 state_dict 사용 |
| `torch.load(path, ...)` | 직접 저장한 파일 읽기 | 파일 경로 | `map_location='cpu'`, `weights_only=True` |
| `model.load_state_dict(state)` | 같은 구조 모델에 상태 적용 | `state_dict` | `strict=True` 기본; shape/키 불일치를 숨기지 않음 |

새로운 실습에서는 위의 옵션을 전부 외우지 않고 코드에 표시된 인자만 바꿉니다.

## v2 변경
실습01~06과 종합 프로젝트 골격은 유지합니다. 총 12개 TODO이며 실습08에서 `day10_stability/tests/test_training.py`의 S11/S12 검증문을 추가로 완성합니다. 평가 함수는 혼합 모드까지 보존하는 제공 코드로 보완했습니다.
