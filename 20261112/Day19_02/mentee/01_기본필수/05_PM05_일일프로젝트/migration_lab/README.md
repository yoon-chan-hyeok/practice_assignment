# Migration 연습 · 기본필수

주 프로젝트 DB `day19_crud_b`와 분리된 `day19_migration_b`에서만 실행합니다.

1. postgres DB에서 `CREATE DATABASE day19_migration_b;`를 한 번 실행합니다.
2. PowerShell에서 현재 폴더로 이동합니다.
3. `$env:MIGRATION_DATABASE_URL="postgresql+psycopg://postgres:비밀번호@localhost:5432/day19_migration_b"`
4. `alembic upgrade 001_initial` → 테이블 확인
5. `alembic upgrade head` → source 열 확인
6. `alembic downgrade 001_initial` → source 제거 확인
7. `alembic upgrade head`로 다시 최신 상태 확인

`stamp`는 실제 DDL을 실행하지 않으므로 이 실습의 복구 명령으로 사용하지 않습니다.
