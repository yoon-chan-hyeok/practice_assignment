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

-- CASE D01
BEGIN;
-- BEGIN H-SQL-13
-- TODO H-SQL-13: C01에서 만든 실제 __NEW_ID__ 행만 DELETE하고 id를 RETURNING하세요. COMMIT 뒤
-- 원래 지식 3건이 모두 그대로 남아야 합니다.
__TODO_H_SQL_13__;
-- END H-SQL-13
COMMIT;
SELECT id FROM public.knowledge WHERE id=__NEW_ID__;
SELECT id,title,content,category_id FROM public.knowledge ORDER BY id;
-- ENDCASE D01
