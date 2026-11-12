# PM04 · Migration과 API·DB 통합 검증

별도 Migration 연습 DB에서 Revision을 적용하고 API 응답 id와 실제 DB 행을 대조합니다.

## 시작
- DB: `day19_crud_a`
- `.env.example` → `.env`, `DB_PASSWORD` 수정
- 서버: `python -m uvicorn app.main:app --reload`
- 문서: `http://127.0.0.1:8000/docs`

## TODO
- 코드 TODO 없음. 실제 데이터로 시나리오를 수행합니다.

## 완료 기준
1. Migration 연습 DB에서 001→002→001→002를 확인합니다.
2. `verify_link.py`로 API와 DB 증거를 같은 id로 대조합니다.
