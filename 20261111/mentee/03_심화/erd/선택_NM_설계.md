# 선택 설계: 한 지식에 여러 태그
PPT 77의 선택 예고입니다. 공통 과제에는 새 테이블을 구현하지 않습니다.
knowledge — knowledge_tags — tags를 그려 보세요.
knowledge_tags(knowledge_id,tag_id)의 복합 PK는 조합 중복을 막고, 개별 ID 반복은 허용합니다.
외래키 두 개의 방향, 삭제 정책을 선택했을 때의 영향을 짧게 설명합니다.
