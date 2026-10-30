# 2026-10-29(목) Day9 실습자료
## GPU · Tensor · Autograd · ANN · 학습 루프

수정된 `Day9_GPU_Tensor_ANN_20261029_v2.pptx`의 실습 01~08에 맞춘 자료입니다. 네 단계를 전부 수행하지 않습니다. **기본필수를 중심으로 시작하고, 응용·심화·특심화는 선택 경로**입니다.

| 단계 | 구조와 범위 | TODO |
|---|---|---:|
| [01_기본필수](01_기본필수/README.md) | 평평한 구조·정상 20건·CPU. 기존 코드와 데이터 그대로 | 9 |
| [02_응용](02_응용/README.md) | data/·outputs/ 구분. 손실 가중 집계와 실제 오답 목록 추가 | 10 |
| [03_심화](03_심화/README.md) | 실습별 구조와 모듈형 프로젝트. 두 검증 테스트 직접 작성 | 12 |
| [04_특심화](04_특심화/README.md) | 교시별 독립 실습 01~08. 상세 요구사항·공개 테스트·결과 보고 | 18 |

기본필수 폴더를 열면 `README.md`, 7개의 `.py`, `points.csv`만 있습니다. 실습 08은 07번 결과를 다시 실행·설명하는 시간입니다. 생성 파일이 추가되어도 원래 코드 파일을 다시 만들 필요가 없습니다.

| 교시 | 주제 | 실습 시간 | PPT 실습 슬라이드 |
|---|---|---:|---:|
| 1 | 환경 점검 | 20분 | 18 |
| 2 | Tensor 모양·자료형·장치 | 25분 | 32 |
| 3 | Autograd·수동 갱신 | 25분 | 43 |
| 4 | ANN·순전파 | 25분 | 54 |
| 5 | 손실·mini-batch | 25분 | 64 |
| 6 | 학습 루프 | 25분 | 74 |
| 7 | 프로젝트 연결 | 25분 | 83 |
| 8 | 재현·설명 | 30분 | 86 |

50분×8교시, 설명·시연 200분 + 실습·리뷰 200분 기준입니다. 기본필수는 PPT 일부 과제를 축소했습니다. 예를 들어 full-batch를 먼저 익히고, mini-batch는 응용부터 다룹니다. 네 단계의 데이터·출력 수치를 섞어 비교하지 마세요.

## 시작 전 준비

이 자료는 Python과 **PyTorch 한 패키지**를 사용합니다. pandas·scikit-learn·torchvision은 필요하지 않습니다. 기존 머신러닝 환경을 지우거나 무조건 업그레이드하지 마세요.

1. VS Code에서 작업할 단계의 폴더를 엽니다. 인터프리터는 강사가 확인한 PyTorch 환경을 선택합니다.
2. 터미널에서 `python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"`를 실행합니다.
3. `ModuleNotFoundError: torch`가 발생하면 같은 인터프리터에 PyTorch가 설치됐는지 강사와 확인합니다. GPU 수업은 공식 설치 선택기에서 OS/Pip/Python/Compute Platform에 맞는 명령을 선택합니다. PPT에 적힌 버전 번호만 보고 CUDA Toolkit이나 드라이버를 임의로 재설치하지 않습니다.
4. GPU를 사용하지 않는 **Windows/Linux CPU 대체 환경**은 `python -m pip install torch --index-url https://download.pytorch.org/whl/cpu`로 준비할 수 있습니다. 이는 GPU 환경 설치 명령이 아닙니다. macOS는 공식 선택기를 사용하세요. 이번 코드는 MPS를 선택하지 않고 CPU 경로로 진행합니다.

Windows PowerShell에서 별도 환경이 필요할 때:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cpu
.venv\Scripts\python.exe -c "import torch; print(torch.__version__)"
```

GPU용 환경은 마지막 두 명령의 설치 부분을 공식 선택기의 해당 명령으로 바꾸고 같은 Python을 사용합니다. PowerShell 실행 정책 때문에 활성화가 막히면 위처럼 `.venv\Scripts\python.exe`를 직접 실행하면 됩니다. 설치가 이미 정상이면 다시 설치하지 마세요.

실제 제작 검수: Python 3.13.5 / PyTorch 2.10.0+cpu / Linux. CUDA 하드웨어 실행과 Windows/macOS 직접 실행은 검증하지 못했습니다. 최신 GPU 패키지와의 동작을 무조건 보장하지 않습니다. GPU용 설치를 CPU 검수 버전으로 덮어쓰라는 뜻도 아닙니다.

## 실행 결과를 읽는 기준

수강생 파일의 `TODO`는 아직 미완성입니다. 기본필수·응용·심화의 임시 값이나 `pass` 때문에 실행이 끝나도 정답은 아닙니다. **예상 출력·코드의 핵심 연산·자신의 설명**을 함께 확인합니다. 특심화는 미완성 함수를 `NotImplementedError`로 명확히 표시합니다.

출력 예시는 CPU 검수 환경의 실제 결과입니다. 무작위 초기값, PyTorch 버전, 장치에 따라 학습 수치는 달라질 수 있습니다. 정확도를 특정 숫자로 맞추는 과제가 아닙니다. shape, 수식, 학습 순서, 장치 일치, 기록 의미를 먼저 확인합니다. 같은 seed라도 CPU/GPU 또는 버전 간 완전 동일성은 보장하지 않습니다.

이번 합성 데이터는 새로운 2차원 ANN 연습 자료입니다. 이전 Day5~8의 요청 로그와 다른 데이터이므로 이전 지표와 비교하지 않습니다. `label = int(x1 + 0.8*x2 > 0)`라는 단순 규칙으로 만들었으나 **학습 코드의 입력은 x1,x2 두 열만**입니다. 이 식을 직접 예측 코드로 쓰면 ANN 학습 과제를 수행한 것이 아닙니다.

고정 분할: 기본필수 20건=12 train+4 valid+4 test, 나머지 단계 200건=120 train+40 valid+40 test. 오늘 test는 입력 Tensor로 만들거나 모델에 넣지 않습니다. train으로 학습하고 valid로 동작을 확인합니다. 매우 작은 합성 자료에서 높은 정확도가 나와도 실제 서비스 성능의 증거가 아닙니다.

80 epoch는 제공된 연습 설정입니다. loss가 매 step마다 반드시 감소해야 한다는 조건은 없습니다. 손실 곡선의 전체 경향, 학습 전후, 평가 표본을 구분합니다. 온라인 학습 손실은 갱신 중 계산한 손실의 가중 평균이고, 고정 모델 평가 손실은 갱신 후 다시 계산한 값입니다.

## 공식 참고자료

기술 설명은 아래 공식 문서와 수업용 실행 검증을 기준으로 작성했습니다. 확인일: 2026-10-27. 문서 최신 버전과 이 자료의 실제 검수 버전은 다를 수 있습니다.

- 설치 선택기: https://pytorch.org/get-started/locally/
- Tensor: https://docs.pytorch.org/docs/stable/generated/torch.tensor.html
- Autograd: https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html
- Linear: https://docs.pytorch.org/docs/stable/generated/torch.nn.Linear.html
- CrossEntropyLoss: https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html
- DataLoader: https://docs.pytorch.org/docs/stable/data.html
- SGD: https://docs.pytorch.org/docs/stable/generated/torch.optim.SGD.html
- 저장·복원: https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html
- 재현성의 범위: https://docs.pytorch.org/docs/stable/notes/randomness.html
- CUDA 동기화: https://docs.pytorch.org/docs/stable/generated/torch.cuda.synchronize.html


## v2에서 달라진 사항

기본필수의 원래 코드·데이터·README는 유지했습니다. 응용의 추가 A09는 샘플 가중 손실, A10은 실제 valid 오답 기록입니다. 심화의 추가 H11·H12는 마지막 작은 배치와 평가의 가중치·gradient 보존 테스트입니다. 특심화는 한 프로젝트의 TODO 목록이 아니라 독립된 **특심화01~08** 폴더입니다.

특심화 각 폴더를 다른 경로에 단독 복사해도 실행할 수 있습니다. 앞 교시 결과·정답 파일을 요구하지 않습니다. 07과 08의 제공 모델/엔진은 선행 학습을 위한 완성 코드이며, 해당 교시의 tasks.py만 새로 구현합니다. 08은 07을 끝내지 않아도 자체 baseline을 생성합니다.

한 사람이 49개 TODO를 모두 하는 과제가 아닙니다. 단계 하나를 선택하여 해당 교시 문제를 풉니다. 기본필수만으로 공통 평가 기준을 충족합니다. GPU 보유나 정답 정확도 절대값은 점수 조건이 아닙니다.

이번 ZIP의 검수 기록은 강사용/운영에 있습니다. 공개 테스트를 제외한 패키지 검수 도구는 수강생에게 과제로 요구하지 않습니다. PPT의 이전 3단계 안내 대신 함께 제공한 v2의 4단계 안내를 사용합니다.
