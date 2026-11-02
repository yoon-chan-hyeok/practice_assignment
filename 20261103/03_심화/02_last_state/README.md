# Padding과 마지막 상태

코드의 공통 모듈 import는 제공된 연결 부분이다. 함수·클래스를 처음부터 새로 설계하지 않는다.

## main.py · Padding과 마지막 상태

PPT 22쪽과 연결한다. 이 실습 폴더를 연다.

```powershell
python main.py
```

### 직접 완성할 부분

- **D02**: 각 자료의 실제 마지막 시점에 해당하는 output을 선택한다.

### 실행 결과 확인

```text
dense 마지막 vs packed: 0.648536
유효 시점 gather vs packed: True
단방향 RNN·eval·우측 Padding의 비교. 양방향은 단순 gather로 대체할 수 없다.
```

**완료 기준**: h_dense가 Padding까지 처리했음을 설명한다.

### 자신의 말로 설명하기

- output과 h_n의 차이는? → 답: ____________________
- 모든 시점의 logits를 쓰려면 어떤 정답 구조가 필요한가? → 답: ____________________

