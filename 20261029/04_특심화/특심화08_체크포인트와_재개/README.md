# 특심화 08 · 체크포인트·복원·새 프로세스 재개

## 학습 목표와 범위
모델·Optimizer·난수·배치 순서를 복원하고 연속 학습과 대조한다.

이 폴더만으로 80회 연속 학습과 40회 저장 후 새 프로세스에서 이어가는 비교가 가능합니다. CPU·동일 버전·epoch 경계·num_workers=0에서 비교합니다. momentum=0.9는 비어 있지 않은 Optimizer state 검사용 제공 설정입니다. 자세한 원리는 Day10에서 배웁니다.

수업 실습 시간: 30분. 처음부터 모든 구현을 새로 설계하는 과제가 아닙니다. **수정할 파일은 `tasks.py`**이며 실행기·데이터·선행 코드·테스트는 제공합니다. 숫자를 하드코딩하거나 expected/를 읽어 결과를 만드는 것은 과제를 수행한 것이 아닙니다.

## 시작 파일과 구조
```text
특심화08_체크포인트와_재개/
  README.md
  tasks.py       # 이번 교시의 직접 구현 부분
  run.py         # 제공 실행기
  tests/         # 공개 정상·경계·실패 검사
  expected/      # 실제 CPU 정답 실행 기록
  reports/       # 본인의 검증·한계 기록
```
07·08에는 로컬 `data/`와 완성된 선행 모델·엔진이 추가됩니다. 다른 실습 폴더나 상위 공통 코드를 import하지 않습니다. `outputs/`는 실행 시 만들어집니다.

## 구현할 요구사항
- **X08-1**: `tasks.py`의 같은 ID 위 주석을 읽고 구현합니다.
- **X08-2**: `tasks.py`의 같은 ID 위 주석을 읽고 구현합니다.
- **X08-3**: `tasks.py`의 같은 ID 위 주석을 읽고 구현합니다.

주석에는 입력·반환값·금지 동작·원본/상태 보존·오류 조건·허용오차를 명시했습니다. 함수/클래스 문법 설명 대신 실제 요구사항을 중심으로 풉니다. 미완성 구현은 `NotImplementedError`로 실패하는 것이 정상입니다.

## 실행 순서
VS Code에서 **이 폴더**를 엽니다. 기존에 확인한 PyTorch 인터프리터를 선택합니다.

```powershell
python -c "import torch; print(torch.__version__)"
python -m unittest discover -s tests -v
python run.py
```

1. 테스트 이름과 요구사항 주석을 먼저 읽고 예상 결과를 기록합니다.
2. TODO 구현 후 공개 테스트를 통과시킵니다. 실제 CUDA 전용 검사는 장치가 없으면 SKIP입니다.
3. run.py를 실행하여 `outputs/resume_report.json`를 만듭니다.
4. expected/와 비교하고 reports/review.md에 확인한 범위와 한계를 적습니다.

테스트는 미완성 상태에서도 문법 오류가 아니라 구현 누락을 알려주도록 구성했습니다. 앞 실습이 미완성이어도 지금 폴더의 과제는 진행할 수 있습니다. 다른 위치에서 실행할 때는 `python "이 폴더의 절대경로/run.py"`를 사용합니다.

## 실제 CPU 참조 출력
```json
{
  "continued_epochs": 80,
  "resumed_from": 40,
  "checks": {
    "schema_version": true,
    "completed_epochs": true,
    "model_state": true,
    "optimizer_state": true,
    "cpu_rng": true,
    "loader_rng": true,
    "cuda_rng": true,
    "config": true,
    "split_ids": true
  },
  "all_equal": true,
  "scope": "same CPU environment; epoch boundary; num_workers=0",
  "test_used": false
}
```

## 완료 기준
구현 ID 3개와 실제 생성 결과를 설명합니다. 공개 검사 4개 중 CPU 확인 가능 검사는 통과해야 합니다. 이번 제작 환경에서 CUDA 전용 미검증 검사는 0개입니다. 학습 수치 자체를 맞추기보다 원리·shape·상태·순서·허용오차를 확인합니다. 타 장치·버전의 bitwise 동일성을 보장한다고 보고하지 않습니다.

## 설명 질문
1. 가중치만 복원하면 학습 재개가 완전히 같은가?
2. 이번 재현 검증을 GPU·다른 버전까지 보장한다고 말할 수 있는가?

## 확장과 실무 연결
정상 입력의 구현 → 명확한 입력 계약 → 결과와 설정 기록 → 반복 가능한 검증 순서로 확장합니다. 실무의 인증·분산 실행·운영 모니터링 전체를 완성한 프로그램은 아닙니다. 실제 GPU·Windows/macOS 실행은 교실에서 별도 확인합니다.

### 08번은 07번의 산출물을 요구하지 않습니다
run.py가 자체 데이터로 기준선과 40회 시점 체크포인트를 만들고, 같은 파일의 `--resume` 모드를 새 Python 프로세스로 실행합니다. 모델·Optimizer·CPU RNG·DataLoader RNG·설정·ID를 비교합니다. 저장은 epoch 경계에서 수행하며 중간 batch·다중 worker 재개는 범위 밖입니다. 자신이 생성한 체크포인트만 읽습니다. 기본필수·응용에는 이 절차를 요구하지 않습니다.
