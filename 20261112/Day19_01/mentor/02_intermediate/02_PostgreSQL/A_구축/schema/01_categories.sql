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
    -- 해설 A-DDL-01: IDENTITY는 번호 생성, PRIMARY KEY는 유일성과 NULL 금지를 담당합니다.
    -- 실패·ROLLBACK으로 번호가 건너뛸 수 있으므로 ID를 행 수로 해석하지 않습니다.
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    -- END A-DDL-01
    -- BEGIN A-DDL-02
    -- 해설 A-DDL-02: categories.name을 VARCHAR(30), 필수, 중복 불가로 선언하세요. 쉼표를 포함합니다.
    name VARCHAR(30) NOT NULL UNIQUE,
    -- END A-DDL-02
    -- BEGIN A-DDL-03
    -- 해설 A-DDL-03: categories_name_length CHECK로 name의 길이를 1~30자로 제한하세요.
    CONSTRAINT categories_name_length CHECK (char_length(name) BETWEEN 1 AND 30)
    -- END A-DDL-03
);
COMMIT;
