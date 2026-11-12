# PM05 · 나만의 PostgreSQL 연동 AI 도움말 API

A 유지·B 수정·C 삭제를 자신의 지식으로 수행하고 서버 재시작·새 DB 연결 뒤 N+2를 확인합니다.

## 시작
- DB: `day19_crud_h`
- `.env.example` → `.env`, `DB_PASSWORD` 수정
- 서버: `python -m uvicorn app.main:app --reload`
- 문서: `http://127.0.0.1:8000/docs`

## TODO
- 코드 TODO 없음. 실제 데이터로 시나리오를 수행합니다.

## 완료 기준
1. 시작 N을 기록합니다.
2. A 유지·B 수정·C 삭제를 API로 수행합니다.
3. SQL로 같은 id를 확인합니다.
4. 서버 재시작·새 DB 연결 뒤 A/B는 남고 C는 없으며 최종 N+2입니다.
