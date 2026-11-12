BEGIN;
-- 제공 안전장치: 아래 DO 구문은 수정 과제가 아닙니다.
DO $guard$
BEGIN
    IF current_database() <> 'day19_build_h' THEN
        RAISE EXCEPTION 'Wrong database: expected day19_build_h, got %', current_database();
    END IF;
END;
$guard$;
-- BEGIN H-DDL-09
-- TODO H-DDL-09: idx_knowledge_category_id라는 비고유 B-tree 인덱스를
-- knowledge(category_id)에 만드세요.
__TODO_H_DDL_09__
-- END H-DDL-09
COMMIT;
