# 제공 준비 SQL — TODO 없음

PPT 부록 A01~A05의 완성된 두 테이블과 가상 초기 데이터입니다.
2교시에 곧바로 SELECT할 수 있게 제공하는 시작점이며, 3교시 _try DDL 과제의 정답을 제출하는 파일이 아닙니다.

| 순서 | 어디에서 | 파일 | 결과 |
|---|---|---|---|
| 0 | postgres DB, 자동 커밋 | 00_create_database.sql | 새 knowledge_lab DB. 이미 있으면 생략/확인 |
| 1 | knowledge_lab DB | 01_prepare_S0.sql | 두 표와 분류 3·지식 3건, 트랜잭션으로 준비 |
| 2 | 같은 DB | 02_check_S0.sql | 목록·분류별 2/1/0·길이 64 확인 |
| 3 | 같은 DB, 필요 시 | 03_inspect_schema.sql | 실제 열·키·제약·인덱스 확인 |

01은 새 빈 표를 만드는 작업입니다. 기존 categories/knowledge가 하나라도 있으면 중단하도록 작성했습니다.
IF NOT EXISTS로 다른 정의를 숨기거나 ON CONFLICT로 잘못된 준비를 덮지 않습니다.
오류가 나면 ROLLBACK만 실행하고 원인을 확인합니다. 준비 성공 후 01을 다시 실행하지 않습니다.
복구·재접속·다음 교시 시작은 Seed 재실행을 의미하지 않습니다.

DDL·Seed 모두 UTF-8입니다. 준비 단계의 DO 블록은 잘못된 DB와 중복 준비를 막는 제공 안전 코드이며
초급자가 직접 작성하거나 문법을 외울 대상이 아닙니다.
