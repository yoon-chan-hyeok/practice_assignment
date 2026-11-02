# 심화 · 모듈형 구조, 구현 부담은 기존 응용 수준

각 단원 폴더에는 `README.md`, `main.py`, `expected/`가 있다. 실행하면 해당 폴더의 `outputs/`가 생긴다. 공통 입력은 이 단계의 `data/`, 제공 모듈은 `day12_sequence_models/`에 있다. **학습 함수와 모델 정의는 제공한다.** 단원별 핵심7곳·프로젝트3곳·계약 테스트2곳=TODO12곳을 작성한다.

- [PackedSequence 왕복](01_packed/README.md): `python 01_packed/main.py`
- [Padding과 마지막 상태](02_last_state/README.md): `python 02_last_state/main.py`
- [가변 길이 LSTM 예측](03_variable_forecast/README.md): `python 03_variable_forecast/main.py`
- [Denoising 입력·target 분리](04_denoising/README.md): `python 04_denoising/main.py`
- [세 구조 같은 자료 비교](05_architectures/README.md): `python 05_architectures/main.py`
- [오류·시간·파라미터 기록](06_errors/README.md): `python 06_errors/main.py`
- [길이별 CPU 비용](07_lengths/README.md): `python 07_lengths/main.py`
- [모듈형 시계열·재구성 프로젝트](day12_sequence_models/README.md): `python day12_sequence_models/main.py`
- [새 프로세스 모델 복원](day12_sequence_models/README.md): `python day12_sequence_models/restore.py`

## 데이터와 분할

이번에는 이미지 대신 새로 만든 정상 사인파·독립 Sequence를 사용한다. 기존 요청 로그와 이미지 자료를 재사용한 것은 아니다. 모든 파일은 UTF-8이다. 결측·중복 ID·잘못된 값 정제는 이번 필수 과제가 아니다.

| 자료 | 기본필수 | 응용·심화·특심화 | 사용 방법 |
|---|---|---|---|
| `series.csv` | 시간순 원관측 100개:60/20/20 | 원관측300개:180/60/60 | 각 시간 구간 안에서 Window 생성 |
| 과거12→다음1 | train48·valid8 | train168·valid48 | test Window는 만들지 않음 |
| 8차원 재구성 | train53·valid13 | train173·valid53 | target=입력8개; Denoising은 clean을 target으로 유지 |
| 독립 Sequence 분류 | 06번 코드의20개:12/4/4 | `sequences.json`100개:60/20/20 | 증가1·감소0, 길이6~12·특성3, ID 기준 독립 |

사인파는 `sin(time*0.23)+0.15*cos(time*0.071)`로 생성했다. 학습용 단순 합성 신호이지 실제 센서의 예측 성능이 아니다. **시간 구간을 먼저 분리하고 그 안에서만 Window를 만든다.** 경계를 넘는 Window와 무작위 Window 분할은 사용하지 않는다. 예측은 이전 관측이 순차적으로 도착하는 one-step 방식이며 여러 시점 재귀 예측과 다르다.

분류 Sequence는 평균이 아니라 증가/감소 순서를 학습하도록 생성했다. 한 시퀀스 안의 시점을 섞지 않는다. 독립 Sequence 사이의 학습 배치 shuffle과 구분한다. `test` 구간/ID는 공통 실습의 학습·선택·예측에 전달하지 않는다.

특심화 **선택 이상탐지 과제만 예외**다. 별도로 생성한 정상 train80·정상/이상 valid40·test40을 사용한다. 정상train으로 AE 학습 → valid로 임계값 확정 → 설정 저장 → 별도 명령으로 해당 test를 한 번 평가한다. 공통 시계열·분류 test를 사용하는 것이 아니다.

## 공식 문서와 실행 환경

API 설명 확인일: 2026-10-25. 실행 검증은 **Python 3.13.5 / torch 2.10.0+cpu / NumPy 2.3.5 / pandas 2.2.3 / Matplotlib 3.10.8 / Linux**이다. PPT의 교육 계획 버전과 실제 검증 버전은 다르다. GPU·Windows·macOS 직접 실행 검증은 하지 않았다.

- RNN: https://docs.pytorch.org/docs/2.13/generated/torch.nn.RNN.html
- LSTM: https://docs.pytorch.org/docs/2.13/generated/torch.nn.LSTM.html
- Padding/Pack: https://docs.pytorch.org/docs/2.13/generated/torch.nn.utils.rnn.pack_padded_sequence.html
- MultiheadAttention: https://docs.pytorch.org/docs/2.13/generated/torch.nn.MultiheadAttention.html
- 설치 선택기: https://pytorch.org/get-started/locally/

공식 API 설명을 참고했지만 실습 데이터·코드·결과표는 이 자료를 위해 직접 작성·실행한 것이다. `stable` 문서의 버전은 바뀔 수 있다. 기본 실습에는 torchvision·GPU·인터넷·사전학습 가중치가 필요하지 않다. 기존 PyTorch 환경이 정상이라면 재설치하지 않는다.

## 최신 수정판 · D11~D12

프로젝트의 `tests/test_contracts.py`에서 평가 상태 보존과 Padding 값 변경 불변성을 검사합니다. 기존 10곳에 2곳을 추가하여 심화는 12개 구현 항목입니다. 프로젝트 폴더에서 `python -m unittest discover -s tests -v`를 실행하세요. 수강생용 `self.fail`은 미완성 표시이므로 검사 없이 지우지 않습니다. `evaluate()`의 원래 모드 복구 코드는 제공했습니다.
