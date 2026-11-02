# Denoising 입력·target 분리

코드의 공통 모듈 import는 제공된 연결 부분이다. 함수·클래스를 처음부터 새로 설계하지 않는다.

## main.py · Denoising 입력·target 분리

PPT 47쪽과 연결한다. 이 실습 폴더를 연다.

```powershell
python main.py
```

### 직접 완성할 부분

- **D04**: 입력만 노이즈를 더하고 정답은 깨끗한 Window로 유지한다.

### 실행 결과 확인

```text
노이즈 입력 자체 MSE: 0.014737
재구성 MSE: 0.014831 best epoch: 40
작은 모델이 입력보다 더 나쁘게 복원할 수도 있다. 개선을 가정하지 않는다.
```

생성 파일: `outputs/denoising.csv`

**완료 기준**: noisy→clean과 clean→clean을 구분한다.

### 자신의 말로 설명하기

- 예측의 target과 재구성의 target은 어떻게 다른가? → 답: ____________________
- 재구성 오류가 높다고 무조건 이상인가? → 답: ____________________

