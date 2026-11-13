# 실습 04 · Transformer 구조·Shape · 응용

**PPT 기준:** 47장. 3단계 중 한 수준을 선택하며, 기본필수도 공통 목표를 충족할 수 있습니다.

**실습 목표:** 출력: transformer_report.json. 이 파일은 수업의 독립 시작점입니다. 앞 교시를 완료하지 못했더라도 이 폴더에서 진행할 수 있습니다.

## 실행

VS Code에서 이 수준의 폴더(`02_intermediate`)를 열고, 프로젝트 최상단에서 다음 명령을 실행하세요.

```powershell
python 04_transformer/main.py
```

활성화 정책으로 가상환경 실행이 막힌다면, 프로젝트의 Python 실행 파일을 명시해서 실행하세요. 예: `.venv\Scripts\python.exe 04_transformer/main.py`.

## TODO 목록 (5개)

1. **D20-04-I01** — Token ID 텐서와 nn.Embedding 출력의 shape (B,T,D)를 구하세요.
2. **D20-04-I02** — EncoderLayer(d_model=8,nhead=2)로 전달하고 shape 보존을 검증하세요.
3. **D20-04-I03** — Residual·LayerNorm·FFN이 바꾸는 값과 보존하는 shape를 기록하세요.
4. **D20-04-I04** — Padding 위치가 attention의 Key/Value에서 제외되지만 출력 위치가 자동 0이 아님을 확인하세요.
5. **D20-04-I05** — 모든 shape와 Mask 의미를 transformer_report.json에 정리하세요.

## 예상 결과 / 확인 기준

Token IDs (2,5) → Token Vectors (2,5,8) → Encoder 출력 (2,5,8). nhead=2는 d_model=8을 나눌 수 있음.

Padding Key Mask는 PAD Query 출력까지 자동 0으로 만들지 않음

**출력 파일:** 실행 시 이 폴더의 `outputs/` 아래에 생성됩니다. 완성 전 `NotImplementedError`가 발생하는 것은 TODO 안내 동작입니다. 예상 결과가 달라지면 원본 데이터를 수정했는지·선택한 모델/시드가 같은지 먼저 확인하세요.

**주의:** 본 실습의 교육용 Tokenizer/Embedding/Logit은 실제 대규모 언어모델의 계산을 단순화한 것입니다. Transformer Tokenizer 및 SentenceTransformer 실제 호출은 루트의 `optional_examples`에서 별도로 안내하며 기본필수 요구사항이 아닙니다.
