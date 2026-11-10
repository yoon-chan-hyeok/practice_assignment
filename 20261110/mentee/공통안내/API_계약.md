# 공통 API 계약 — PPT 21·48·59쪽

이 자료는 **84장 일일프로젝트 포함 수정본**을 기준으로 합니다. 상품 API·4단계 구판을 사용하지 않습니다.
서비스의 목적은 **RAG·AI Agent 플랫폼의 원본 지식 관리 기반**입니다. 지금은 AI 모델·RAG·Agent를 실행하지 않습니다.

| 요청 | 입력 | 정상 응답 |
|---|---|---|
| GET /health | 없음 | 200, {"status":"ok"} |
| GET /api/knowledge | 응용·심화: 선택 category Query | 200, 지식 배열 |
| GET /api/knowledge/{knowledge_id} | 정수 ID | 200, 지식 한 건 |
| POST /api/knowledge | title·content·category 모두 | 201, 서버가 발급한 id 포함 |
| PUT /api/knowledge/{knowledge_id} | 정수 ID + 세 필드 모두 | 200, 같은 id를 유지한 지식 |
| DELETE /api/knowledge/{knowledge_id} | 정수 ID | 204, 응답 본문 없음 |

`title`: 1~80자, `content`: 1~2000자, `category`: 1~30자입니다. 세 필드에 기본값이 없으므로 모두 필수입니다.
`category`는 자유 문자열입니다. `setup`·`api`만 허용하는 열거형이 아닙니다.
공백만 있는 문자열은 현재 길이 규칙만으로는 거절되지 않습니다. 추가 입력 필드는 Pydantic 기본 설정으로 무시됩니다.
반드시 공백 제거·엄격 모드·추가 필드 거절까지 구현해야 하는 과제가 아닙니다.

정수지만 없는 ID는 404와 `{"detail":"Knowledge not found"}`입니다. `foo`와 같은 정수가 아닌 Path, 필수 값 누락, 빈 본문은 기본 422입니다.
404를 확인할 때에는 PUT Body를 정상으로 보냅니다. Body까지 틀리면 422가 먼저 나올 수 있습니다.
PUT은 부분 수정이 아닙니다. 없는 ID의 PUT으로 새 데이터를 만들지도 않습니다.
삭제한 ID를 다시 GET 또는 DELETE하면 404입니다. 삭제해도 next_id는 줄이지 않습니다.
category를 생략하면 전체 목록, 일치하지 않으면 200과 빈 목록입니다. 단순 문자열 필터를 RAG 검색이라고 부르지 않습니다.

## 저장과 확인

초기 파일은 next_id=4, entries에는 ID 1·2·3이 있습니다. 목록 응답은 entries만 내보내며 내부 next_id는 포함하지 않습니다.
POST가 성공하면 entries와 next_id를 함께 저장합니다. PUT과 DELETE는 next_id를 바꾸지 않습니다.
서버 시작 시 초기 데이터를 자동 복사하지 않습니다. 서버 종료·재시작은 데이터 초기화가 아닙니다.
교시별 폴더는 서로 다른 파일을 사용합니다. 폴더를 바꿔서 데이터가 달라지는 것은 저장 실패가 아닙니다.

이것은 로컬 단일 프로세스 학습용입니다. 외부 공개, 인증·권한, 여러 workers, 전원 장애 내구성, DB 트랜잭션은 구현 범위가 아닙니다.
파일은 실행 중 외부 편집기로 수정하지 않습니다. API 키·실제 개인정보·내부 문서는 쓰지 않습니다.
