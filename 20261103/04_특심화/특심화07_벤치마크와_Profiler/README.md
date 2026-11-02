# 특심화 07 · 성능 측정·상태 보존·Profiler

## 목표와 시간
현재 교시 주제의 정확성과 검증 책임을 직접 구현합니다. 핵심 구현 2개를 먼저 진행하고 남은 항목은 README의 선택 확장으로 수행합니다. 예시 운영: 요구사항 확인5분 → 핵심 구현12~15분 → 테스트·기록5분. 08은30분의 통합·재현 활동입니다.

## 파일 역할
`tasks.py`만 구현합니다. `run.py`·`support.py`·필요한 `models.py/data.py`는 제공 코드입니다. `tests/`는 공개 검사, `expected/`는 강사 CPU 실행 비교용 결과, `reports/review.md`는 본인 해석입니다. `outputs/`는 실행할 때 생성됩니다. 경로 전체를 복사해도 해당 폴더만으로 실행합니다.

|구현 ID|함수|확인할 것|
|---|---|---|
|`X07-1`|`measure(model, x, lengths, repeats=5, warmup=2, training=False)`|함수 위 계약과 공개 테스트를 함께 확인|
|`X07-2`|`profile_workload(model, cpu_x, lengths, device)`|함수 위 계약과 공개 테스트를 함께 확인|
|`X07-3`|`summarize_runs(rows)`|함수 위 계약과 공개 테스트를 함께 확인|

## 시작·실행
```powershell
python -m pytest tests -q
python run.py
```
수강생의 `NotImplementedError`는 미완성 표시입니다. 정답 숫자를 하드코딩하거나 검사를 지우지 마세요. 강사용은 같은 위치에 완성된 구현과 추가 해설을 제공합니다.

## 결과와 확인 기준
`outputs/timing_raw.csv` 18행, `timing_summary.csv` 9행. `--profile`은 `trace.json`·`profiler_check.json`을 추가합니다.
`expected/stdout.txt`와 수치·행 개수·상태 확인을 대조하세요. 마지막 소수점은 버전 영향이 있을 수 있어 코드에 지정한 허용오차를 사용합니다. 시간·처리량은 같아야 하는 정답 숫자가 아닙니다. 테스트 성공은 공개한 조건에 한하며 운영환경의 무오류를 보장하지 않습니다.

## 설명 질문
1. 입력·출력·실제 길이와 Padding의 역할을 한 문장씩 쓰세요.
2. 검사한 수치 외에 원본·모드·gradient·난수 중 무엇을 보존해야 합니까?
3. 성공한 검사와 미검증 환경을 분리해서 기록하세요. 실제 GPU 실행이 없다면 GPU 통과라고 쓰지 않습니다.


### 선택: Profiler / CUDA
`python run.py --profile`은 실제 CPU trace와 4개 구간 이름을 기록합니다. GPU가 준비된 환경에서만 `python run.py --device cuda --profile`을 사용합니다. 명시적으로 cuda를 요청했는데 장치가 없으면 오류이며 CPU 결과로 위장하지 않습니다. 전송 제외의 모델 구간과 데이터 공급 포함의 profiler 구간은 별도 표입니다.

## 참고
PyTorch 공식 문서: https://docs.pytorch.org/docs/2.10/profiler.html
원본 데이터는 수업용 합성 자료입니다. 출처를 가진 코드/모델만 사용하고, 자기 실행으로 생성한 checkpoint만 복원하세요.
