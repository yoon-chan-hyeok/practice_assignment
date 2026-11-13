# 실습 07 · LLM 한계·검증·RAG/Agent · 응용

**PPT 기준:** 76장. 3단계 중 한 수준을 선택하며, 기본필수도 공통 목표를 충족할 수 있습니다.

**실습 목표:** 출력: review.json / review.md. 이 파일은 수업의 독립 시작점입니다. 앞 교시를 완료하지 못했더라도 이 폴더에서 진행할 수 있습니다.

## 실행

VS Code에서 이 수준의 폴더(`02_intermediate`)를 열고, 프로젝트 최상단에서 다음 명령을 실행하세요.

```powershell
python 07_limits/main.py
```

활성화 정책으로 가상환경 실행이 막힌다면, 프로젝트의 Python 실행 파일을 명시해서 실행하세요. 예: `.venv\Scripts\python.exe 07_limits/main.py`.

## TODO 목록 (5개)

1. **D20-07-I01** — 3개 답변에서 정해 둔 형태·근거·사실 불일치를 분류하세요.
2. **D20-07-I02** — 사실성·형식·근거 검증을 서로 다른 검사라고 설명하세요.
3. **D20-07-I03** — 각 실패 유형에 Prompt·RAG·DB/API 검증 중 대응을 매칭하세요.
4. **D20-07-I04** — 같은 답변이라도 출처가 틀릴 수 있으므로 추가 점검 항목을 제시하세요.
5. **D20-07-I05** — 검증 결과와 향후 후속 수업 연결을 review.json 및 review.md로 저장하세요.

## 예상 결과 / 확인 기준

F01=factual_mismatch(원본과 불일치), F02=format(필수 sources 누락), F03=evidence(출처 미기재).

형식 검증 통과와 사실 검증 통과는 독립이며, 실제 LLM 답변 자동 평가로 오해하지 않음

**출력 파일:** 실행 시 이 폴더의 `outputs/` 아래에 생성됩니다. 완성 전 `NotImplementedError`가 발생하는 것은 TODO 안내 동작입니다. 예상 결과가 달라지면 원본 데이터를 수정했는지·선택한 모델/시드가 같은지 먼저 확인하세요.

**주의:** 본 실습의 교육용 Tokenizer/Embedding/Logit은 실제 대규모 언어모델의 계산을 단순화한 것입니다. Transformer Tokenizer 및 SentenceTransformer 실제 호출은 루트의 `optional_examples`에서 별도로 안내하며 기본필수 요구사항이 아닙니다.
