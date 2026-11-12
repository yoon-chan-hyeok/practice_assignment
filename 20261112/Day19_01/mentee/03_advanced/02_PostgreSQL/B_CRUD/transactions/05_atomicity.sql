-- 제공 안전장치: 아래 DO 구문은 수정 과제가 아닙니다.
DO $guard$
BEGIN
    IF current_database() <> 'day19_crud_h' THEN
        RAISE EXCEPTION 'Wrong database: expected day19_crud_h, got %', current_database();
    END IF;
END;
$guard$;
-- 파일 전체 실행 금지: 조회는 CASE 단위, 변경은 BEGIN → DML RETURNING → 종료문 → SELECT를 각각 선택합니다.
-- __NEW_ID__는 C01 RETURNING으로 받은 실제 정수로 치환합니다. 구현 TODO와 다릅니다.

-- CASE T01
BEGIN;
-- BEGIN H-SQL-14
-- TODO H-SQL-14: 한 트랜잭션 안에서 ID 1·2의 본문을 각각 임시 내용 1·임시 내용 2로 바꾸세요. 제공된 ROLLBACK
-- 뒤 두 원문이 모두 유지되어야 합니다.
__TODO_H_SQL_14__
-- END H-SQL-14
ROLLBACK;
SELECT id,content FROM public.knowledge WHERE id IN (1,2) ORDER BY id;
-- ENDCASE T01
