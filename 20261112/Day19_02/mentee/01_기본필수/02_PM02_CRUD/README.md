# PM02 · 기존 API 계약을 PostgreSQL CRUD로 연결

GET·POST·PUT·DELETE 다섯 API를 PostgreSQL CRUD로 연결합니다.

## 시작
- DB: `day19_crud_b`
- `.env.example` → `.env`, `DB_PASSWORD` 수정
- 서버: `python -m uvicorn app.main:app --reload`
- 문서: `http://127.0.0.1:8000/docs`

## TODO
- **B04** · `app/main.py` · 분류 문자열을 내부 category_id로 연결하세요.
- **B05** · `app/main.py` · 상세 조회와 404 계약을 완성하세요.
- **B06** · `app/main.py` · POST의 DB INSERT와 201 응답을 연결하세요.
- **B07** · `app/main.py` · PUT 전체 수정과 DB UPDATE를 연결하세요.
- **B08** · `app/main.py` · DELETE와 빈 204 응답을 완성하세요.

## 완료 기준
1. 목록·상세·생성·수정·삭제가 동작합니다.
2. POST 응답의 실제 id를 SQL로 조회하면 같은 행이 있습니다.
3. DELETE 뒤 같은 id의 DB 행은 0개입니다.
