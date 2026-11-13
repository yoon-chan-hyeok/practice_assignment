# 실습 06 · 학습·추론·Sampling · 심화

**PPT 기준:** 68장. 3단계 중 한 수준을 선택하며, 기본필수도 공통 목표를 충족할 수 있습니다.

**실습 목표:** 출력: inference_report.json. 이 파일은 수업의 독립 시작점입니다. 앞 교시를 완료하지 못했더라도 이 폴더에서 진행할 수 있습니다.

## 실행

VS Code에서 이 수준의 폴더(`03_advanced`)를 열고, 프로젝트 최상단에서 다음 명령을 실행하세요.

```powershell
python 06_inference/main.py
```

활성화 정책으로 가상환경 실행이 막힌다면, 프로젝트의 Python 실행 파일을 명시해서 실행하세요. 예: `.venv\Scripts\python.exe 06_inference/main.py`.

## TODO 목록 (9개)

1. **D20-06-A01** — Logit[2,1,0]을 Softmax로 바꾸어 확률의 합이 1인지 확인하세요.
2. **D20-06-A02** — Temperature 0.5·1.0·2.0에서 확률 분포를 비교하세요.
3. **D20-06-A03** — Greedy로 다음 Token 후보를 선택하고 학습/추론 차이를 기록하세요.
4. **D20-06-A04** — Top-k(k=2)의 후보 집합과 정규화된 확률을 구하세요.
5. **D20-06-A05** — 같은 seed로 확률 샘플링을 재현하고 Greedy와 차이를 설명하세요.
6. **D20-06-A06** — Top-p(p=0.75)에 포함되는 최소 후보 집합을 계산하세요.
7. **D20-06-A07** — 작은 선형 모델 한 번의 학습 단계에서 파라미터가 바뀌는지 확인하세요.
8. **D20-06-A08** — KV Cache가 저장하는 것·저장하지 않는 것과 비용을 설명하세요.
9. **D20-06-A09** — 확률·선택·학습/추론 차이를 inference_report.json에 기록하세요.

## 예상 결과 / 확인 기준

Logits [2,1,0]의 Softmax는 약 [0.665,0.245,0.090], 확률합=1. Greedy는 후보 A.

Temperature만 바꿔 비교하고 Sampling 결과는 난수 시드에 의존함

**출력 파일:** 실행 시 이 폴더의 `outputs/` 아래에 생성됩니다. 완성 전 `NotImplementedError`가 발생하는 것은 TODO 안내 동작입니다. 예상 결과가 달라지면 원본 데이터를 수정했는지·선택한 모델/시드가 같은지 먼저 확인하세요.

**주의:** 본 실습의 교육용 Tokenizer/Embedding/Logit은 실제 대규모 언어모델의 계산을 단순화한 것입니다. Transformer Tokenizer 및 SentenceTransformer 실제 호출은 루트의 `optional_examples`에서 별도로 안내하며 기본필수 요구사항이 아닙니다.
