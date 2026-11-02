# 특심화 04 · DataLoader와 순서·Worker 재현성

## 목표
샘플 누락 없는 배치와 seed를 가진 로더를 구성하고 시작 비용과 반복 사용 비용을 구분한다.

PPT 47쪽 실습과 연결합니다. 수강생용: tasks.py를 직접 구현합니다.

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
- **X04-1**: `tasks.py`의 같은 번호 주석에 있는 계약을 구현합니다.
- **X04-2**: `tasks.py`의 같은 번호 주석에 있는 계약을 구현합니다.

### 다중 Worker 선택 실행
```powershell
python run.py --workers 2
```
이 경로도 Linux CPU에서 실행 검증했습니다. Windows/macOS는 직접 미검증이며 `if __name__ == "__main__":`를 제거하지 않습니다. 입력은 실제 PNG 60장이고 변환은 결정적입니다. 결과의 `scope`는 **host decode/transform/collate**이며 GPU 대기시간을 직접 측정한 것이 아닙니다. 첫 epoch와 둘째 epoch를 구분합니다.

## 데이터·산출물·완료 기준
기존 Day11 train60·valid20 이미지를 이 폴더에 독립 복사했습니다. test는 포함하지 않습니다.

주요 산출물: `outputs/loader_benchmark.csv`, `outputs/loader_order.json`.
`expected/stdout.txt`와 다음 출력을 비교합니다. 소수 오차의 기준은 tests와 tasks에 있으며 시간·처리량·Profiler 내부 시간은 실행마다 달라집니다.

```text
workers: 0 이미지: 60 배치: [16, 16, 16, 12]
새 loader의 첫 epoch 순서 일치: True host 로딩만 측정; GPU 대기시간 아님
```

구현을 완료하고 공개 테스트를 실행한 뒤 `run.py`의 결과를 직접 생성합니다. `reports/review.md`에 **고정 조건·관찰 결과·근거·미검증 항목**을 적고 설명합니다. 예상 결과 파일을 복사하는 것으로 완료 처리하지 않습니다.

## 설명 질문
1. Worker를 늘렸는데 첫 epoch가 느려질 수 있는 이유는?
2. shuffle 순서가 같아도 random transform 값이 항상 같은가?

## 검증 범위
제작 실행 환경은 Python 3.13.5·torch 2.10.0+cpu·torchvision 0.25.0+cpu·Linux입니다. 실제 NVIDIA CUDA·Windows/macOS는 미검증입니다. 사전학습 모델 성능은 가중치 실행 여부를 별도 표시합니다. 작은 합성 이미지의 결과를 실제 서비스 성능으로 일반화하지 않습니다.

`expected/loader_*`는 기본 workers=0 실행, `expected/workers2_*`는 실제 spawn workers=2 실행 기록입니다. 시간은 고정 정답이 아닙니다.
