# PM03 · 실패한 요청에서도 데이터 보호

IntegrityError·rollback·503을 구분하고 실패 뒤 데이터 보존을 확인합니다.

## 시작
- DB: `day19_crud_h`
- `.env.example` → `.env`, `DB_PASSWORD` 수정
- 서버: `python -m uvicorn app.main:app --reload`
- 문서: `http://127.0.0.1:8000/docs`

## TODO
- **H13** · `app/services/knowledge_service.py` · 제약조건 이름 기반의 안전한 오류 분류를 구현하세요.
- **H14** · `app/main.py` · 도메인 오류를 HTTP 409로 변환하세요.
- **H15** · `app/main.py` · DB 연결 상태까지 확인하는 health를 구현하세요.

## 완료 기준
1. 422 요청에서 DB가 바뀌지 않습니다.
2. DB 제약 실패 뒤 rollback되어 Session이 복구됩니다.
3. DB 연결 실패와 일반 API 오류를 구분합니다.
