# 강사용 제작 검증 기록

멘토의 3개 수준 × 8개 교시 = 24개 진입점 실행, CPU 수치·Output 조건 확인.
수강생의 TODO 30 / 46 / 63개가 강사용 마커 139개에 1:1 대응합니다.

- 교육용 ToyTokenizer(사전학습 모델 아님): A/B/C Token 수 8/7/9
- Cosine: A/B 약 0.9701, A/C -1.0
- EncoderLayer: (2,5)→(2,5,8)→(2,5,8)
- Causal Attention: 미래 가중치 0, 행 합 1
- Logit [2,1,0] Softmax: 약 0.665/0.245/0.090
- 사실/형식/근거 실패 유형: F01/F02/F03 구분

실행 환경: Python 3.13, PyTorch 2.10.0+CPU, NumPy 2.3.5, Matplotlib 3.10.8.
Windows 11·VS Code 상호작용과 선택 HuggingFace 모델 다운로드·실행은 **이 환경에서 직접 검수하지 않았습니다.**
