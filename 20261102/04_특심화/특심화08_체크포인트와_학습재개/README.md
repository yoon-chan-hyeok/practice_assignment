# 특심화 08 · 체크포인트·독립 프로세스 학습 재개

## 목표
epoch 경계에서 중단하고 새 프로세스로 재개한 학습을 연속 실행과 전체 저장 상태로 비교한다.

PPT 87쪽 실습과 연결합니다. 수강생용: tasks.py를 직접 구현합니다.

## 공통 실행·제출 규칙
이 폴더에서 `tasks.py`의 현재 교시 구현 항목만 작성합니다. 이전 특심화의 정답·결과 파일은 필요하지 않습니다. 제공된 `support.py`·실행기·데이터·테스트도 같이 복사하면 **이 폴더만 단독 실행**할 수 있습니다.

20~30분 실습에서는 핵심 두 문제부터 진행합니다. 07·08의 세 번째 문제는 선택 확장/통합 검증으로 이어갈 수 있습니다. 이번 시간을 못 끝냈어도 다음 교시 폴더를 독립적으로 시작합니다. `expected/`는 출력 비교용이지 프로그램 입력이 아닙니다. 정답 수치나 파일 경로를 하드코딩하지 않습니다.

함수·클래스 문법은 전공자 수준으로 가정합니다. 함수 바로 위 주석의 **입력·반환값·금지 동작·상태 보존·실패 조건·허용오차**가 구현 계약입니다. `NotImplementedError`는 미완성 표시입니다. 그 아래에 숨긴 정답은 없습니다.

```text
README.md             # 진행 순서·완료 기준
 tasks.py              # 직접 구현하는 요구사항
 run.py                # 제공된 실행기
 support.py            # 완성된 선행 기능
 tests/                # 공개 계약 테스트
 expected/             # 실제 CPU 참조 출력
 reports/review.md      # 조건·결과·판단·한계
 data/                 # 필요한 실습에만 train/valid 이미지
 outputs/              # 실행 때 생성, 배포 시 제외
```

기존 torch·torchvision 가상환경을 재사용하고 정상 CUDA 환경을 CPU 패키지로 덮어쓰지 않습니다. VS Code에서 이 폴더를 열고 터미널에서 실행합니다.

```powershell
python -c "import torch, torchvision; print(torch.__version__, torchvision.__version__)"
python -m unittest discover -s tests -v
python run.py
```

테스트 실패 메시지에서 첫 번째 문제를 확인하고 함수 요구사항으로 돌아갑니다. 기본 실행은 CPU에서 가능합니다. CUDA는 실제 장치가 있을 때만 측정합니다. CUDA 없음은 실패가 아니라 **SKIP/N/A**이며 0초·0MiB 같은 가짜 측정값을 쓰지 않습니다.

## 직접 구현할 문제
- **X08-1**: `tasks.py`의 같은 번호 주석에 있는 계약을 구현합니다.
- **X08-2**: `tasks.py`의 같은 번호 주석에 있는 계약을 구현합니다.
- **X08-3**: `tasks.py`의 같은 번호 주석에 있는 계약을 구현합니다.

### 새 프로세스 재개 검증
`run.py`가 `worker.py`를 세 번 별도 프로세스로 실행합니다. 4회 연속 / 2회 후 저장 / 새 프로세스에서 남은 2회 학습의 순서입니다. 데이터 hash·config 검사가 먼저이며, 모델과 Optimizer를 만든 뒤 RNG를 마지막에 복원합니다.

`.pt` 파일은 `outputs/`에서 직접 생성합니다. 인터넷에서 출처 불명의 checkpoint를 읽지 않습니다. 각 결과의 `history.json`과 `resume_comparison.json`을 비교하세요. 범위는 **동일 CPU·버전·1 thread·workers=0·epoch 경계**입니다. 다중 Worker prefetch나 mid-epoch 재개까지 보장하지 않습니다.

## 데이터·산출물·완료 기준
기존 Day11 train60·valid20 이미지를 이 폴더에 독립 복사했습니다. test는 포함하지 않습니다.

주요 산출물: `outputs/resume_comparison.json`.
`expected/stdout.txt`와 다음 출력을 비교합니다. 소수 오차의 기준은 tests와 tasks에 있으며 시간·처리량·Profiler 내부 시간은 실행마다 달라집니다.

```text
마친 epoch: 4 train 이미지/epoch: 60 test 미사용
마친 epoch: 2 train 이미지/epoch: 60 test 미사용
마친 epoch: 4 train 이미지/epoch: 60 test 미사용
4회 연속 vs 2+새 프로세스+2 전체 상태 일치: True
```

구현을 완료하고 공개 테스트를 실행한 뒤 `run.py`의 결과를 직접 생성합니다. `reports/review.md`에 **고정 조건·관찰 결과·근거·미검증 항목**을 적고 설명합니다. 예상 결과 파일을 복사하는 것으로 완료 처리하지 않습니다.

## 설명 질문
1. 모델 weight만 복원하면 학습 재개가 완전한가?
2. mid-epoch·다중 Worker·다른 CUDA 환경까지 정확 일치를 일반화할 수 있는가?

## 검증 범위
제작 실행 환경은 Python 3.13.5·torch 2.10.0+cpu·torchvision 0.25.0+cpu·Linux입니다. 실제 NVIDIA CUDA·Windows/macOS는 미검증입니다. 사전학습 모델 성능은 가중치 실행 여부를 별도 표시합니다. 작은 합성 이미지의 결과를 실제 서비스 성능으로 일반화하지 않습니다.

## 체크포인트 안전성
이 실습의 완전 상태 파일은 본인이 직접 생성한 **신뢰하는 체크포인트만** 읽습니다. 임의의 인터넷 `.pt` 파일에 `weights_only=False`를 사용하지 않습니다. 사전학습 가중치는 별도 공식 출처 준비 경로를 따릅니다.
