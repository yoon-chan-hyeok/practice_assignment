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

-- CASE U01
BEGIN;
-- BEGIN H-SQL-11
-- TODO H-SQL-11: C01의 실제 __NEW_ID__ 행만 content='복습 자료와 예제 코드를 함께 확인합니다.'로
-- UPDATE하고 id·content를 RETURNING하세요. 뒤의 ROLLBACK 후 원문이 남아야 합니다.
__TODO_H_SQL_11__;
-- END H-SQL-11
ROLLBACK;
SELECT id,content FROM public.knowledge WHERE id=__NEW_ID__;
-- ENDCASE U01

-- CASE U02
BEGIN;
-- BEGIN H-SQL-12
-- TODO H-SQL-12: C01의 실제 __NEW_ID__ 행에 같은 본문 수정을 실행하세요. 뒤의 COMMIT 후 변경한 본문이
-- 남아야 합니다.
__TODO_H_SQL_12__;
-- END H-SQL-12
COMMIT;
SELECT id,content FROM public.knowledge WHERE id=__NEW_ID__;
-- ENDCASE U02
