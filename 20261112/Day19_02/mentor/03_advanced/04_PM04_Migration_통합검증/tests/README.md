# 심화 · PostgreSQL Test DB 통합 검사

1. postgres DB에서 `CREATE DATABASE day19_test_h;`를 한 번 실행합니다.
2. `prepare_test_schema.sql`을 **day19_test_h**에서 실행합니다.
3. PowerShell: `$env:TEST_DATABASE_URL="postgresql+psycopg://postgres:비밀번호@localhost:5432/day19_test_h"`
4. `pytest -q`

개발/오전 DB를 테스트 대상으로 사용하지 않습니다. 이 테스트는 실제 PostgreSQL이 있을 때만 실행합니다.
