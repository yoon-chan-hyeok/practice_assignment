BEGIN;
-- 제공 안전장치: 아래 DO 구문은 수정 과제가 아닙니다.
DO $guard$
BEGIN
    IF current_database() <> 'day19_build_h' THEN
        RAISE EXCEPTION 'Wrong database: expected day19_build_h, got %', current_database();
    END IF;
END;
$guard$;
CREATE TABLE public.categories (
    -- BEGIN H-DDL-01
    -- TODO H-DDL-01: categories.id의 BIGINT·ALWAYS IDENTITY·PK를 선언하세요.
    __TODO_H_DDL_01__
    -- END H-DDL-01
    -- BEGIN H-DDL-02
    -- TODO H-DDL-02: categories.name의 VARCHAR(30)·NOT NULL·UNIQUE를 선언하세요.
    __TODO_H_DDL_02__
    -- END H-DDL-02
    -- BEGIN H-DDL-03
    -- TODO H-DDL-03: categories_name_length CHECK를 작성하세요.
    __TODO_H_DDL_03__
    -- END H-DDL-03
);
COMMIT;
