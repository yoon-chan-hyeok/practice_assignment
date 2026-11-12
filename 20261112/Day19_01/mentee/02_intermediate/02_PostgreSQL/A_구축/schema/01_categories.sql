BEGIN;
-- 제공 안전장치: 아래 DO 구문은 수정 과제가 아닙니다.
DO $guard$
BEGIN
    IF current_database() <> 'day19_build_a' THEN
        RAISE EXCEPTION 'Wrong database: expected day19_build_a, got %', current_database();
    END IF;
END;
$guard$;
CREATE TABLE public.categories (
    -- BEGIN A-DDL-01
    -- TODO A-DDL-01: categories.id를 BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY
    -- KEY로 선언하세요. 쉼표를 포함합니다.
    __TODO_A_DDL_01__
    -- END A-DDL-01
    -- BEGIN A-DDL-02
    -- TODO A-DDL-02: categories.name을 VARCHAR(30), 필수, 중복 불가로 선언하세요. 쉼표를 포함합니다.
    __TODO_A_DDL_02__
    -- END A-DDL-02
    -- BEGIN A-DDL-03
    -- TODO A-DDL-03: categories_name_length CHECK로 name의 길이를 1~30자로 제한하세요.
    __TODO_A_DDL_03__
    -- END A-DDL-03
);
COMMIT;
