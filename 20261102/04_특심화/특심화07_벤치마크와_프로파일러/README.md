# 특심화 07 · 반복 벤치마크와 단계별 프로파일링

## 목표
같은 모델 초기 상태·입력·정밀도·측정 범위에서 반복 측정하고 profiler를 별도 관찰 자료로 쓴다.

PPT 81쪽 실습과 연결합니다. 수강생용: tasks.py를 직접 구현합니다.

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
- **X07-1**: `tasks.py`의 같은 번호 주석에 있는 계약을 구현합니다.
- **X07-2**: `tasks.py`의 같은 번호 주석에 있는 계약을 구현합니다.
- **X07-3**: `tasks.py`의 같은 번호 주석에 있는 계약을 구현합니다.

### Profiler 선택 실행
```powershell
python run.py --profile
```
`outputs/trace.json`은 Chrome trace 형식입니다. `profile_report.json`에 주요 이벤트를 기록합니다. 프로파일링에는 관측 비용이 추가되므로 일반 benchmark 시간과 섞지 않습니다. 벤치마크는 같은 초기 state·새 Optimizer·seed·미리 적재한 CPU batch·3회 반복·워밍업 1회 조건입니다. 파일 I/O는 제외하고 H2D/forward/backward/step은 포함합니다. CPU VRAM은 null입니다. trace를 공개할 때 로컬 경로를 검토합니다.

## 데이터·산출물·완료 기준
기존 Day11 train60·valid20 이미지를 이 폴더에 독립 복사했습니다. test는 포함하지 않습니다.

주요 산출물: `outputs/compute_benchmark.csv`, `outputs/profile_report.json`, `outputs/timing_summary.json`.
`expected/stdout.txt`와 다음 출력을 비교합니다. 소수 오차의 기준은 tests와 tasks에 있으며 시간·처리량·Profiler 내부 시간은 실행마다 달라집니다.

```text
cpu channels_last= False measured
cpu channels_last= True measured
cuda channels_last= False SKIP_NO_CUDA
cuda channels_last= True SKIP_NO_CUDA
원본 모델/RNG 보존, CUDA 미가용은 SKIP; 시간은 실행마다 달라진다.
```

구현을 완료하고 공개 테스트를 실행한 뒤 `run.py`의 결과를 직접 생성합니다. `reports/review.md`에 **고정 조건·관찰 결과·근거·미검증 항목**을 적고 설명합니다. 예상 결과 파일을 복사하는 것으로 완료 처리하지 않습니다.

## 설명 질문
1. 파일 I/O 포함 측정과 사전 적재 측정을 왜 구분해야 하는가?
2. profiler 시간과 일반 wall time을 같은 표에서 순위 매겨도 되는가?

## 검증 범위
제작 실행 환경은 Python 3.13.5·torch 2.10.0+cpu·torchvision 0.25.0+cpu·Linux입니다. 실제 NVIDIA CUDA·Windows/macOS는 미검증입니다. 사전학습 모델 성능은 가중치 실행 여부를 별도 표시합니다. 작은 합성 이미지의 결과를 실제 서비스 성능으로 일반화하지 않습니다.
