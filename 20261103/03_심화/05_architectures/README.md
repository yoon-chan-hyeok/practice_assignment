# 세 구조 같은 자료 비교

코드의 공통 모듈 import는 제공된 연결 부분이다. 함수·클래스를 처음부터 새로 설계하지 않는다.

## main.py · 세 구조 같은 자료 비교

PPT 58쪽과 연결한다. 이 실습 폴더를 연다.

```powershell
python main.py
```

### 직접 완성할 부분

- **D05**: 후보 name에 해당하는 실제 아키텍처를 생성한다.

### 실행 결과 확인

```text
model  params  best_epoch  valid_loss  accuracy
        RNN     746          25    0.001468       1.0
       LSTM     842          25    0.043251       1.0
Transformer    1162          25    0.028943       1.0
```

생성 파일: `outputs/architecture_comparison.csv`

**완료 기준**: 파라미터 수는 비슷한 범위이지 동일하지 않음을 기록한다.

### 자신의 말로 설명하기

- key Padding과 query 집계 제외를 왜 둘 다 하는가? → 답: ____________________
- head별 weight와 head 평균 weight의 shape 차이는? → 답: ____________________

