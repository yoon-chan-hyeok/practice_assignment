# 길이별 CPU 비용

코드의 공통 모듈 import는 제공된 연결 부분이다. 함수·클래스를 처음부터 새로 설계하지 않는다.

## main.py · 길이별 CPU 비용

PPT 81쪽과 연결한다. 이 실습 폴더를 연다.

```powershell
python main.py
```

### 직접 완성할 부분

- **D07**: 실제로 측정한 20회 전체의 샘플 수로 throughput을 계산한다.

### 실행 결과 확인

아래 값 중 시간·처리량은 검수 PC의 관측 예시이다. **정답 숫자로 맞추지 않는다.** 같은 모델·데이터라도 실행 부하로 달라진다.

```text
model  length  seconds    samples_s device peak_vram
        RNN      16 0.003580 89396.661928    cpu      None
       LSTM      16 0.007062 45313.462248    cpu      None
Transformer      16 0.007051 45380.968980    cpu      None
        RNN      32 0.005717 55972.756660    cpu      None
       LSTM      32 0.010520 30418.592148    cpu      None
Transformer      32 0.010557 30312.827432    cpu      None
        RNN      64 0.009174 34880.281065    cpu      None
       LSTM      64 0.020400 15686.431374    cpu      None
Transformer      64 0.026750 11962.405748    cpu      None
측정: CPU 순전파 / 워밍업 제외 / 배치16 / 반복20 / GPU VRAM 미측정
```

생성 파일: `outputs/lengths.csv`

**완료 기준**: 속도 순위를 일반화하지 말고 실제 조건을 함께 적는다.

### 자신의 말로 설명하기

- 측정에 forward/backward/H2D/로딩 중 무엇이 포함됐나? → 답: ____________________
- CPU에서 VRAM을0이 아니라 N/A로 적는 이유는? → 답: ____________________

