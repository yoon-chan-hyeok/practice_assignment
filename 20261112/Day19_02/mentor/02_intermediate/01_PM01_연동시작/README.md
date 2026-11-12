# PM01 · 설정부터 실제 PostgreSQL 목록 조회

DB 설정·Session Dependency·첫 ORM 목록 조회를 완성합니다.

## 시작
- DB: `day19_crud_a`
- `.env.example` → `.env`, `DB_PASSWORD` 수정
- 서버: `python -m uvicorn app.main:app --reload`
- 문서: `http://127.0.0.1:8000/docs`

## TODO
- 코드 TODO 없음. 실제 데이터로 시나리오를 수행합니다.

## 완료 기준
1. `SELECT current_database()`와 API가 같은 DB를 가리킵니다.
2. 오전 SQL로 만든 지식이 GET 목록에서 보입니다.
