# 실습 08 · 문장 하나가 LLM 출력이 되기까지 · 응용

**PPT 기준:** 82장. 3단계 중 한 수준을 선택하며, 기본필수도 공통 목표를 충족할 수 있습니다.

**실습 목표:** 출력: daily_project.json / one_page_summary.md. 이 파일은 수업의 독립 시작점입니다. 앞 교시를 완료하지 못했더라도 이 폴더에서 진행할 수 있습니다.

## 실행

VS Code에서 이 수준의 폴더(`02_intermediate`)를 열고, 프로젝트 최상단에서 다음 명령을 실행하세요.

```powershell
python 08_daily_project/main.py
```

활성화 정책으로 가상환경 실행이 막힌다면, 프로젝트의 Python 실행 파일을 명시해서 실행하세요. 예: `.venv\Scripts\python.exe 08_daily_project/main.py`.

## TODO 목록 (8개)

1. **D20-08-I01** — 공통 지식 A의 문장을 Token·ID로 분석하고 Token 수·Context 제한을 기록하세요.
2. **D20-08-I02** — 교육용 벡터 A/B/C의 Cosine 표를 만들고 비슷한 방향을 찾아보세요.
3. **D20-08-I03** — Q/K/V 3×2 Attention에 Causal Mask를 적용하고 행 합=1·미래 가중치=0을 확인하세요.
4. **D20-08-I04** — Logit→Softmax→Greedy 다음 Token 선택 흐름을 구현하세요.
5. **D20-08-I05** — 개인 문장 세 개를 바꾸어 입력 길이·padding과 truncation 상태를 비교하세요.
6. **D20-08-I06** — Mask 없는 Attention과 Causal Attention의 차이를 정량 비교하세요.
7. **D20-08-I07** — PPT의 네 단계와 플랫폼 연결 그림을 Markdown으로 완성하세요.
8. **D20-08-I08** — Token·Cosine·Attention·Logit 검증 결과를 종합 JSON으로 저장하세요.

## 예상 결과 / 확인 기준

공통 A/B/C를 재사용하여 Token·Cosine·3×3 Causal Attention·Logit→Softmax→선택·플랫폼 연결을 한 번에 완성.

기본필수로도 공통 100점: Token/Context 25, Embedding 20, Attention 25, 학습/추론 15, 플랫폼 연결 15

**출력 파일:** 실행 시 이 폴더의 `outputs/` 아래에 생성됩니다. 완성 전 `NotImplementedError`가 발생하는 것은 TODO 안내 동작입니다. 예상 결과가 달라지면 원본 데이터를 수정했는지·선택한 모델/시드가 같은지 먼저 확인하세요.

**주의:** 본 실습의 교육용 Tokenizer/Embedding/Logit은 실제 대규모 언어모델의 계산을 단순화한 것입니다. Transformer Tokenizer 및 SentenceTransformer 실제 호출은 루트의 `optional_examples`에서 별도로 안내하며 기본필수 요구사항이 아닙니다.
