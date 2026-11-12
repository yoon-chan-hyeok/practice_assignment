# Day19 오후 · FastAPI–PostgreSQL 연동 실습

오전에는 FastAPI와 PostgreSQL을 각각 다뤘습니다. 오후에는 **같은 API 요청이 실제 PostgreSQL 행을 조회·변경하도록 연결**합니다.

## 공통 API 계약
- GET `/api/knowledge`
- GET `/api/knowledge/{knowledge_id}`
- POST `/api/knowledge` → 201
- PUT `/api/knowledge/{knowledge_id}` → 200
- DELETE `/api/knowledge/{knowledge_id}` → 204, Body 없음
- 입력: `title`, `content`, `category`
- 없는 ID: 404 / 입력 검증: 422

## 중요한 전제
- 오전 DB를 자동 초기화하지 않습니다.
- 실제 생성 ID는 응답에서 받아 후속 요청과 SQL 조회에 사용합니다.
- 외부 API의 `category` 문자열은 DB 내부 `category_id`와 동일한 것이 아닙니다.
- 주 프로젝트 DB, Migration 연습 DB, 테스트 DB는 구분합니다.
