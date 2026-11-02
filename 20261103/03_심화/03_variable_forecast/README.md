# 가변 길이 LSTM 예측

코드의 공통 모듈 import는 제공된 연결 부분이다. 함수·클래스를 처음부터 새로 설계하지 않는다.

## main.py · 가변 길이 LSTM 예측

PPT 34쪽과 연결한다. 이 실습 폴더를 연다.

```powershell
python main.py
```

### 직접 완성할 부분

- **D03**: 후보의 packed 설정을 모델에 적용해 valid MSE를 비교한다.

### 실행 결과 확인

```text
packed  best_epoch  valid_mse
  False          30   0.123487
   True          30   0.003160
dense는 마지막 Padding 상태를 쓰는 진단용 비교이며 권장 구현이 아니다.
```

생성 파일: `outputs/variable_comparison.csv`

**완료 기준**: 동일 Window target과 학습 조건에서 Padding 영향만 비교한다.

### 자신의 말로 설명하기

- 과거12개 중 정답이 섞여 있지는 않은가? → 답: ____________________
- LSTM의 h와 c를 구분할 수 있는가? → 답: ____________________

