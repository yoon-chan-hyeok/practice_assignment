# 실습 05 · Self-Attention·Mask·Heatmap · 기본필수

**PPT 기준:** 58장. 3단계 중 한 수준을 선택하며, 기본필수도 공통 목표를 충족할 수 있습니다.

**실습 목표:** 출력: attention_report.json, 응용·심화는 attention_heatmap.png. 이 파일은 수업의 독립 시작점입니다. 앞 교시를 완료하지 못했더라도 이 폴더에서 진행할 수 있습니다.

## 실행

VS Code에서 이 수준의 폴더(`01_basic`)를 열고, 프로젝트 최상단에서 다음 명령을 실행하세요.

```powershell
python 05_attention/main.py
```

활성화 정책으로 가상환경 실행이 막힌다면, 프로젝트의 Python 실행 파일을 명시해서 실행하세요. 예: `.venv\Scripts\python.exe 05_attention/main.py`.

## TODO 목록 (4개)

1. **D20-05-B01** — Scaled Dot-Product Q@K.T/sqrt(d_k)로 (3,3) Score를 계산하세요.
2. **D20-05-B02** — 미래 Key를 차단하는 upper-triangle Causal Mask를 작성하세요.
3. **D20-05-B03** — Score를 Softmax Weight로 바꾸고 Mask된 칸=0, 행 합=1을 확인하세요.
4. **D20-05-B04** — Score·Causal Mask·Weight·행 합과 Output을 JSON으로 저장하세요.

## 예상 결과 / 확인 기준

PPT Weight: [[1,0,0],[약0.33,약0.67,0],[약0.25,약0.25,약0.50]]. 각 행 합=1, 위쪽 마스크 가중치=0.

Score/Weight를 구분하고 Heatmap의 행 Query, 열 Key를 반대로 쓰지 않음

**출력 파일:** 실행 시 이 폴더의 `outputs/` 아래에 생성됩니다. 완성 전 `NotImplementedError`가 발생하는 것은 TODO 안내 동작입니다. 예상 결과가 달라지면 원본 데이터를 수정했는지·선택한 모델/시드가 같은지 먼저 확인하세요.

**주의:** 본 실습의 교육용 Tokenizer/Embedding/Logit은 실제 대규모 언어모델의 계산을 단순화한 것입니다. Transformer Tokenizer 및 SentenceTransformer 실제 호출은 루트의 `optional_examples`에서 별도로 안내하며 기본필수 요구사항이 아닙니다.
