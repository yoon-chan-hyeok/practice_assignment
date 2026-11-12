# PM04 · Migration과 API·DB 통합 검증

별도 Migration 연습 DB에서 Revision을 적용하고 API 응답 id와 실제 DB 행을 대조합니다.

## 시작
- DB: `day19_crud_h`
- `.env.example` → `.env`, `DB_PASSWORD` 수정
- 서버: `python -m uvicorn app.main:app --reload`
- 문서: `http://127.0.0.1:8000/docs`

## TODO
- **H16** · `verify_link.py` · API와 DB 증거를 같은 id로 연결하세요.
- **H17** · `verify_link.py` · DELETE의 실제 DB 반영을 검증하세요.
- **M06** · `migration_lab/migrations/versions/002_source.py` · upgrade에서 source 열을 추가하세요.
- **M07** · `migration_lab/migrations/versions/002_source.py` · source 인덱스를 추가하세요.
- **M08** · `migration_lab/migrations/versions/002_source.py` · downgrade 순서를 안전하게 작성하세요.
- **M09** · `migration_lab/migrations/versions/002_source.py` · 연습 DB에만 적용되는지 확인 절차를 README에 기록하세요.

- **H18** · `tests/test_integration.py` · Test DB Session Dependency를 완성하세요.
- **H19** · `tests/test_integration.py` · API 응답 id로 실제 Test DB Row를 검증하세요.

## 완료 기준
1. Migration 연습 DB에서 001→002→001→002를 확인합니다.
2. `verify_link.py`로 API와 DB 증거를 같은 id로 대조합니다.
