# PM01 · 설정부터 실제 PostgreSQL 목록 조회

DB 설정·Session Dependency·첫 ORM 목록 조회를 완성합니다.

## 시작
- DB: `day19_crud_h`
- `.env.example` → `.env`, `DB_PASSWORD` 수정
- 서버: `python -m uvicorn app.main:app --reload`
- 문서: `http://127.0.0.1:8000/docs`

## TODO
- **H01** · `app/settings.py` · 설정 객체에서 안전한 DB URL을 만드세요.
- **H02** · `app/db.py` · Engine 생성 책임을 구현하세요.
- **H03** · `app/db.py` · Session Factory를 구현하세요.
- **H04** · `app/db.py` · Session 수명과 연결 반환을 구현하세요.
- **H05** · `app/repositories/knowledge.py` · Repository 조회를 완성하세요.

## 완료 기준
1. `SELECT current_database()`와 API가 같은 DB를 가리킵니다.
2. 오전 SQL로 만든 지식이 GET 목록에서 보입니다.
