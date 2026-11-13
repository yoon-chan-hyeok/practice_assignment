# 실습 01 · AI 서비스 구성요소 연결 · 기본필수

**PPT 기준:** 15장. 3단계 중 한 수준을 선택하며, 기본필수도 공통 목표를 충족할 수 있습니다.

**실습 목표:** 출력: architecture.md / architecture.json. 이 파일은 수업의 독립 시작점입니다. 앞 교시를 완료하지 못했더라도 이 폴더에서 진행할 수 있습니다.

## 실행

VS Code에서 이 수준의 폴더(`01_basic`)를 열고, 프로젝트 최상단에서 다음 명령을 실행하세요.

```powershell
python 01_ecosystem/main.py
```

활성화 정책으로 가상환경 실행이 막힌다면, 프로젝트의 Python 실행 파일을 명시해서 실행하세요. 예: `.venv\Scripts\python.exe 01_ecosystem/main.py`.

## TODO 목록 (3개)

1. **D20-01-B01** — FastAPI·PostgreSQL·LLM·응답의 역할 네 가지를 짧은 문장으로 작성하세요.
2. **D20-01-B02** — 요청→API→데이터·LLM→응답 연결을 올바른 순서의 화살표로 표현하세요.
3. **D20-01-B03** — 완성한 연결 관계를 Mermaid 그림과 JSON 요약으로 저장하세요.

## 예상 결과 / 확인 기준

기본필수: API·DB·LLM·응답의 역할과 화살표 설명. 응용: Retriever·EvidenceCheck 추가. 심화: ToolPermission·신뢰 경계까지 설명.

웹/API/DB/LLM/RAG/Agent 역할을 혼동하지 않으며, 개념도의 미래 단계는 미구현으로 표시

**출력 파일:** 실행 시 이 폴더의 `outputs/` 아래에 생성됩니다. 완성 전 `NotImplementedError`가 발생하는 것은 TODO 안내 동작입니다. 예상 결과가 달라지면 원본 데이터를 수정했는지·선택한 모델/시드가 같은지 먼저 확인하세요.

**주의:** 본 실습의 교육용 Tokenizer/Embedding/Logit은 실제 대규모 언어모델의 계산을 단순화한 것입니다. Transformer Tokenizer 및 SentenceTransformer 실제 호출은 루트의 `optional_examples`에서 별도로 안내하며 기본필수 요구사항이 아닙니다.
