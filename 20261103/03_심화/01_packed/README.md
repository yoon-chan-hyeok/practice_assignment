# PackedSequence 왕복

코드의 공통 모듈 import는 제공된 연결 부분이다. 함수·클래스를 처음부터 새로 설계하지 않는다.

## main.py · PackedSequence 왕복

PPT 12쪽과 연결한다. 이 실습 폴더를 연다.

```powershell
python main.py
```

### 직접 완성할 부분

- **D01**: 정렬되지 않은 길이 [4,2,5]를 그대로 pack한다. 힌트: lengths는 CPU의 양수 정수이다. enforce_sorted=False로 내부 정렬을 허용한다.

### 실행 결과 확인

```text
packed data: (11, 3) batch_sizes: [3, 3, 2, 2, 1]
복원: (3, 5, 3) [4, 2, 5]
원본 일치: True
```

**완료 기준**: 11개의 유효 시점과 원래 배치 순서 복원을 확인한다.

### 자신의 말로 설명하기

- B·T·F가 각각 무엇인가? → 답: ____________________
- Padding의 0과 실제 관측값0을 어떻게 구분하는가? → 답: ____________________

