# PM02 · 기존 API 계약을 PostgreSQL CRUD로 연결

GET·POST·PUT·DELETE 다섯 API를 PostgreSQL CRUD로 연결합니다.

## 시작
- DB: `day19_crud_a`
- `.env.example` → `.env`, `DB_PASSWORD` 수정
- 서버: `python -m uvicorn app.main:app --reload`
- 문서: `http://127.0.0.1:8000/docs`

## TODO
- **A05** · `app/repositories/knowledge.py` · Repository 상세 조회를 구현하세요.
- **A06** · `app/repositories/knowledge.py` · 분류 생성 정책을 구현하세요.
- **A07** · `app/repositories/knowledge.py` · Repository 생성 함수를 구현하세요.
- **A08** · `app/routers/knowledge.py` · POST 흐름을 연결하세요.
- **A09** · `app/routers/knowledge.py` · PUT을 DB UPDATE에 연결하세요.
- **A10** · `app/routers/knowledge.py` · DELETE 흐름을 완성하세요.

## 완료 기준
1. 목록·상세·생성·수정·삭제가 동작합니다.
2. POST 응답의 실제 id를 SQL로 조회하면 같은 행이 있습니다.
3. DELETE 뒤 같은 id의 DB 행은 0개입니다.
