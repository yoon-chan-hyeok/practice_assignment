BEGIN;
-- 제공 안전장치: 아래 DO 구문은 수정 과제가 아닙니다.
DO $guard$
BEGIN
    IF current_database() <> 'day19_build_b' THEN
        RAISE EXCEPTION 'Wrong database: expected day19_build_b, got %', current_database();
    END IF;
END;
$guard$;
CREATE TABLE public.categories (
    -- BEGIN B-DDL-01
    -- 해설 B-DDL-01: IDENTITY는 번호 생성, PRIMARY KEY는 유일성과 NULL 금지를 담당합니다.
    -- 실패·ROLLBACK으로 번호가 건너뛸 수 있으므로 ID를 행 수로 해석하지 않습니다.
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    -- END B-DDL-01
    name VARCHAR(30) NOT NULL UNIQUE,
    -- BEGIN B-DDL-02
    -- 해설 B-DDL-02: categories.name의 1~30자 길이 CHECK를 categories_name_length라는 이름으로
    -- 완성하세요.
    CONSTRAINT categories_name_length CHECK (char_length(name) BETWEEN 1 AND 30)
    -- END B-DDL-02
);
CREATE TABLE public.knowledge (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title VARCHAR(80) NOT NULL,
    content TEXT NOT NULL,
    category_id BIGINT NOT NULL,
    -- BEGIN B-DDL-03
    -- 해설 B-DDL-03: NOT NULL과 길이 CHECK는 다른 규칙입니다. 빈 문자열은 NULL이 아니므로 길이 하한으로 막습니다.
    -- 제목 중복 금지나 공백 제거를 이 요구사항에 추가하지 않습니다.
    CONSTRAINT knowledge_title_length CHECK (char_length(title) BETWEEN 1 AND 80),
    CONSTRAINT knowledge_content_length CHECK (char_length(content) BETWEEN 1 AND 2000),
    -- END B-DDL-03
    CONSTRAINT knowledge_category_fk FOREIGN KEY (category_id)
        -- BEGIN B-DDL-04
        -- 해설 B-DDL-04: FK는 실제 부모 존재를 검사합니다. category_id의 NOT NULL과 함께 필수 관계를 만들고
        -- RESTRICT는 참조 중인 부모 삭제를 막습니다. FK가 JOIN 결과를 자동으로 만들지는 않습니다.
        REFERENCES public.categories(id) ON DELETE RESTRICT
        -- END B-DDL-04
);
COMMIT;
