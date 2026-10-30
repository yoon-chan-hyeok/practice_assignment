# Day9 특심화 · 교시별 독립 실습 01~08

각 교시 폴더는 독립 실행됩니다. 이전 과제의 완성 코드나 생성 파일을 가져올 필요가 없습니다. Python·PyTorch만 필요하며 unittest는 표준 라이브러리입니다.

| 교시 | 주제 | 구현 위치·ID | 결과물 |
|---|---|---|---|
| 01 | [환경설정과 장치 정책](특심화01_환경설정과_장치정책/README.md) | tasks.py · X01-1, X01-2 | environment.json |
| 02 | [Tensor 계약과 이동](특심화02_Tensor계약과_이동/README.md) | tasks.py · X02-1, X02-2 | tensor_contract.json |
| 03 | [해석 미분·수치 미분·Autograd](특심화03_미분검증/README.md) | tasks.py · X03-1, X03-2 | gradient_check.json |
| 04 | [모델 구조와 동등성](특심화04_모델구조와_동등성/README.md) | tasks.py · X04-1, X04-2 | model_contract.json |
| 05 | [안정적 손실과 배치 집계](특심화05_손실과_배치집계/README.md) | tasks.py · X05-1, X05-2 | loss_contract.json |
| 06 | [학습과 평가의 분리](특심화06_학습과_평가계약/README.md) | tasks.py · X06-1, X06-2 | engine_contract.json |
| 07 | [ANN 파이프라인 통합](특심화07_ANN파이프라인/README.md) | tasks.py · X07-1, X07-2, X07-3 | final_metrics.json |
| 08 | [체크포인트·복원·새 프로세스 재개](특심화08_체크포인트와_재개/README.md) | tasks.py · X08-1, X08-2, X08-3 | resume_report.json |

**총 8개 실습·18개 구현 항목**입니다. 01~06은 해당 개념의 독립 실험, 07은 데이터→학습→기록 통합, 08은 자체 baseline과 체크포인트 재개 비교입니다. 통합 프로젝트 하나를 8개 이름으로 복사한 방식이 아닙니다.

코드 주석의 입력·반환·불변 조건·실패 정책을 우선 읽습니다. 각 폴더의 공개 테스트는 표준 `unittest`로 실행합니다. 특심화03의 수치미분과 08의 재귀 상태 비교는 시간이 남을 때 확장할 수 있습니다. 강사는 완료한 실습만 확인하고 모든 단계를 하루에 강제하지 않습니다.

CPU를 기본 검수 경로로 두며 NVIDIA GPU가 없어도 시작할 수 있습니다. 01·02의 실제 CUDA 검사는 장치가 없으면 SKIP으로 남깁니다. 07의 선택 CUDA 실행과 08의 CPU 재개 동일성 검증 범위를 혼동하지 않습니다.
