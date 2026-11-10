# 참고 MVP · Knowledge API

TODO 없는 완성형 최소 서비스입니다. 수강생 과제와 별도 제공하며, 전체 흐름을 먼저 보거나 수업 후 참고할 때 사용합니다.
RAG·AI Agent 플랫폼의 원본 지식을 관리하는 기반입니다. RAG 검색·LLM 답변·Agent 실행을 구현한 것은 아닙니다.

## 실행

이 폴더를 VS Code에서 열고 터미널의 현재 위치도 이 폴더로 맞춥니다.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

`http://127.0.0.1:8000/docs`에서 실행합니다. Linux/macOS는 `.venv/bin/python`을 사용합니다.

## 역할

- app/main.py: 앱 생성, Router 등록, /health.
- app/schemas.py: title 1~80자, content 1~2000자, category 1~30자. 세 필드 모두 필수.
- app/routers/knowledge.py: HTTP Method·Path·상태코드.
- app/repositories/json_knowledge.py: JSON 파일 접근·ID 발급·CRUD.
- data/knowledge.json: 현재 지식·next_id. knowledge.seed.json: 명시적 초기화용 원본.
- tests: 실제 작업 파일이 아닌 임시 파일을 쓰는 검증.

## API

GET /api/knowledge (선택 category), GET /api/knowledge/{knowledge_id}, POST /api/knowledge,
PUT /api/knowledge/{knowledge_id}, DELETE /api/knowledge/{knowledge_id}.
정상 200·201·204, 없는 ID 404, 잘못된 입력 422. DELETE 204에는 본문이 없습니다.
입력 Body는 {"title":"실습 안내", "content":"로컬 폴더를 확인합니다.", "category":"setup"}처럼 작성합니다.
서버 응답의 id를 기록해 후속 요청에서 사용합니다. PUT은 세 필드를 모두 보냅니다.

POST → GET → PUT → 같은 서버 종료·재시작 → GET → DELETE → 재시작 → GET 404를 확인합니다.
처음부터 같은 학습 데이터를 여러 서버로 동시에 열지 않습니다. 서버를 시작할 때 데이터를 초기화하지 않습니다.

## 선택 테스트

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-test.txt
.\.venv\Scripts\python.exe -m pytest -q
```

실제 재시작 확인은 TestClient 검사와 별도입니다. 초기화가 필요하면 서버 종료 후 `python reset_data.py --confirm-reset`을 명시적으로 실행합니다.
원본 파일이 손상되었을 때 자동으로 빈 데이터로 덮어쓰지 않습니다. 단일 프로세스 Lock·임시 파일 교체는 DB 트랜잭션·운영 내구성을 대체하지 않습니다.
인증·권한·외부 공개·DB·LLM 호출은 구현하지 않았습니다. 실제 비밀과 개인정보를 넣지 않습니다.
