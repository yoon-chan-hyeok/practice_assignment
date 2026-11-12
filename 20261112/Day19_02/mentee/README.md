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

## 난이도
- **01_기본필수**: 단순한 app 구조에서 제공 골격의 핵심 TODO를 완성합니다. 수동 /docs + SQL 대조가 공통 완료 기준입니다.
- **02_응용**: Router와 Repository를 분리하고 category 필터와 검증 코드를 조금 더 직접 작성합니다.
- **03_심화**: Router·Service·Repository로 역할을 나누고 제약 이름 기반 오류 분류·통합 검증을 보완합니다.