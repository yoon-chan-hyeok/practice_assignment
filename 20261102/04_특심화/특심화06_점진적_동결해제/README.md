# 특심화 06 · 점진적 동결 해제와 Optimizer 계약

## 목표
사전학습 모델의 학습 범위를 Head에서 layer4로 확장할 때 상태·BatchNorm·파라미터 그룹을 점검한다.

PPT 70쪽 실습과 연결합니다. 수강생용: tasks.py를 직접 구현합니다.

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
- **X06-1**: `tasks.py`의 같은 번호 주석에 있는 계약을 구현합니다.
- **X06-2**: `tasks.py`의 같은 번호 주석에 있는 계약을 구현합니다.

### 구조 검사와 실제 전이학습을 구분
기본 `python run.py`는 **ResNet18(weights=None)의 구조·동결 검사**입니다. 정확도·전이 성능 결과가 아닙니다. Head는 2클래스이므로 학습 파라미터 1,026개, Partial은 BN affine을 제외한 layer4+Head를 계산합니다.

```powershell
python run.py --pretrained
```
이 선택 경로는 **공식 ImageNet 가중치 다운로드/캐시**가 필요합니다. 현재 제작 환경에서는 다운로드가 차단되어 실행 미검증입니다. 무작위 가중치로 자동 대체하지 않습니다. 교실에서 준비한 뒤 같은 data/train의 실제 사전학습 모델 경로를 실행합니다. 현재 학생에게 요구하는 핵심은 상태 전환·Optimizer·BN 계약이며 전체 자연 사진 성능 비교는 별도 과제입니다.

## 데이터·산출물·완료 기준
기존 Day11 train60·valid20 이미지를 이 폴더에 독립 복사했습니다. test는 포함하지 않습니다.

주요 산출물: `outputs/freeze_contract.csv`, `outputs/parameters_head.csv`, `outputs/parameters_partial.csv`.
`expected/stdout.txt`와 다음 출력을 비교합니다. 소수 오차의 기준은 tests와 tasks에 있으며 시간·처리량·Profiler 내부 시간은 실행마다 달라집니다.

```text
  stage  actual_pretrained  trainable_params  groups  changed_parameters  bn_buffers_unchanged
   head              False              1026       1                   2                  True
partial              False           8389634       2                   7                  True
STRUCTURE ONLY: weights=None. 전이 성능/정확도 결과가 아니다.
```

구현을 완료하고 공개 테스트를 실행한 뒤 `run.py`의 결과를 직접 생성합니다. `reports/review.md`에 **고정 조건·관찰 결과·근거·미검증 항목**을 적고 설명합니다. 예상 결과 파일을 복사하는 것으로 완료 처리하지 않습니다.

## 설명 질문
1. requires_grad=False만으로 BN running statistics가 고정되는가?
2. unfreeze할 때 Optimizer를 새로 만들면 기존 moment는 어떻게 되는가?

## 검증 범위
제작 실행 환경은 Python 3.13.5·torch 2.10.0+cpu·torchvision 0.25.0+cpu·Linux입니다. 실제 NVIDIA CUDA·Windows/macOS는 미검증입니다. 사전학습 모델 성능은 가중치 실행 여부를 별도 표시합니다. 작은 합성 이미지의 결과를 실제 서비스 성능으로 일반화하지 않습니다.
