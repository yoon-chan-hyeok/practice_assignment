# 아키텍처 비교 보고서

1. 문제: 예측·재구성·분류의 입력과 target을 각각 설명한다.
2. 분할: 시간 구간을 먼저 나눈 이유, Window 수, 독립 ID 분할을 적는다.
3. 구조: RNN·LSTM·Transformer의 params·hidden·mask·position·손실을 비교한다.
4. 수치: architecture_comparison.csv에서 best epoch·valid 지표를 인용한다.
5. 오류: predictions.csv 또는 classification_predictions.csv의 실제 ID를 사용한다. 오류가 없으면 0건으로 적고 만들어내지 않는다.
6. 비용: 측정 장치와 시간 범위, GPU 미측정/N/A, 소표본 변동을 적는다.
7. 재현: 실행 명령·버전·restore_check.csv 결과·본인 Git 기록을 남긴다.
8. 한계: 합성 자료·반복 valid 조회·test 미사용·실제 서비스 평가 계획을 설명한다.
