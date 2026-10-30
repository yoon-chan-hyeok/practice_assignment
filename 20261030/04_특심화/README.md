# Day10 특심화 · 교시별 독립 실습 01~08

각 시간에 같은 핵심 개념을 더 엄밀하게 구현·검증합니다. 이전 `day10_lab` 한 프로젝트 방식은 사용하지 않습니다. 다음 번호의 시작에 이전 번호의 완료 파일이 필요하지 않습니다.

|교시|폴더|구현 항목|주제|
|---|---|---:|---|
|1|[특심화01_Optimizer와_대응실험](특심화01_Optimizer와_대응실험/README.md)|2|Optimizer·대응 seed 실험|
|2|[특심화02_학습률과_Scheduler](특심화02_학습률과_Scheduler/README.md)|2|학습률·Scheduler 호출 계약|
|3|[특심화03_Batch와_기울기누적](특심화03_Batch와_기울기누적/README.md)|2|Batch·정확한 기울기 누적|
|4|[특심화04_학습곡선과_반복진단](특심화04_학습곡선과_반복진단/README.md)|2|반복 학습곡선·best epoch 진단|
|5|[특심화05_MC_Dropout과_모드](특심화05_MC_Dropout과_모드/README.md)|2|Monte Carlo Dropout·상태 보존|
|6|[특심화06_정규화와_WeightDecay](특심화06_정규화와_WeightDecay/README.md)|2|BatchNorm·LayerNorm·Weight Decay|
|7|[특심화07_EarlyStopping_통합](특심화07_EarlyStopping_통합/README.md)|3|Early Stopping·학습 안정화 통합|
|8|[특심화08_체크포인트와_재개](특심화08_체크포인트와_재개/README.md)|3|체크포인트·새 프로세스 재개|

전체 8개 실습·18개 구현 항목입니다. 문제 수와 TODO 수는 다릅니다. 07은 학습 안정화의 통합, 08은 자기 실행에서 만든 체크포인트의 새 프로세스 재개로 목적을 구분합니다. 각 폴더 README→tasks.py 주석→공개 테스트→run.py→보고서 순서로 진행합니다.
