# Day15 · 심화
코드 난이도는 기존 응용 수준입니다. 폴더는 실습·제공 계산 모듈·프로젝트로 역할을 나눴습니다.
`provided/`는 제공 코드로 읽기 참고용이며 새로 모두 구현하는 과제가 아닙니다.
입력은 `data/`, 각 실습의 결과는 해당 `outputs/`, 예상 결과는 `expected/`입니다.
각 실습 폴더의 README를 먼저 읽습니다. 04→05의 checkpoint 비교는 실제 앞 학습 파일이 필요합니다.
07~08은 `day15_detection`을 이어 사용합니다. 이 프로젝트는 자기 data 폴더가 있어 단독 복사해도 경로를 계산합니다.
실제 YOLO는 제작 환경에서 실행 미검증이며, 별도 설치·준비 모델이 필요합니다.

| 순서 | 파일 | 내용 |
|---|---|---|
|01|01_coordinates/main.py|clip·면적|
|02|02_ap/main.py|교육용 AP101|
|03|03_groups/main.py|그룹 분할|
|04|04_train/main.py|YOLO imgsz 비교|
|05|05_checkpoint/main.py|04의 best·last 비교|
|06|06_errors/main.py|오류 유형 원리|
|07|day15_detection/main.py|실제 탐지·추적 통합|
|08|day15_detection/restore.py|새 프로세스 복원|
