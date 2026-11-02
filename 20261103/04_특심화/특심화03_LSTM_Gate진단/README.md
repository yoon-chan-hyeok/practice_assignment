# 특심화 03 · LSTM gate와 유효 시점 진단

## 목표와 시간
현재 교시 주제의 정확성과 검증 책임을 직접 구현합니다. 핵심 구현 2개를 먼저 진행하고 남은 항목은 README의 선택 확장으로 수행합니다. 예시 운영: 요구사항 확인5분 → 핵심 구현12~15분 → 테스트·기록5분. 08은30분의 통합·재현 활동입니다.

## 파일 역할
`tasks.py`만 구현합니다. `run.py`·`support.py`·필요한 `models.py/data.py`는 제공 코드입니다. `tests/`는 공개 검사, `expected/`는 강사 CPU 실행 비교용 결과, `reports/review.md`는 본인 해석입니다. `outputs/`는 실행할 때 생성됩니다. 경로 전체를 복사해도 해당 폴더만으로 실행합니다.

|구현 ID|함수|확인할 것|
|---|---|---|
|`X03-1`|`trace_lstm(cell, x, h0=None, c0=None)`|함수 위 계약과 공개 테스트를 함께 확인|
|`X03-2`|`summarize_gates(gate_log, lengths)`|함수 위 계약과 공개 테스트를 함께 확인|

## 시작·실행
```powershell
python -m pytest tests -q
python run.py
```
수강생의 `NotImplementedError`는 미완성 표시입니다. 정답 숫자를 하드코딩하거나 검사를 지우지 마세요. 강사용은 같은 위치에 완성된 구현과 추가 해설을 제공합니다.

## 결과와 확인 기준
`outputs/gate_summary.csv`: i/f/g/o 네 행. 각 행의 count=24(실제 시점8×hidden3).
`expected/stdout.txt`와 수치·행 개수·상태 확인을 대조하세요. 마지막 소수점은 버전 영향이 있을 수 있어 코드에 지정한 허용오차를 사용합니다. 시간·처리량은 같아야 하는 정답 숫자가 아닙니다. 테스트 성공은 공개한 조건에 한하며 운영환경의 무오류를 보장하지 않습니다.

## 설명 질문
1. 입력·출력·실제 길이와 Padding의 역할을 한 문장씩 쓰세요.
2. 검사한 수치 외에 원본·모드·gradient·난수 중 무엇을 보존해야 합니까?
3. 성공한 검사와 미검증 환경을 분리해서 기록하세요. 실제 GPU 실행이 없다면 GPU 통과라고 쓰지 않습니다.


## 참고
PyTorch 공식 문서: https://docs.pytorch.org/docs/2.10/generated/torch.nn.LSTM.html
원본 데이터는 수업용 합성 자료입니다. 출처를 가진 코드/모델만 사용하고, 자기 실행으로 생성한 checkpoint만 복원하세요.
