BEGIN;
-- 제공 안전장치: 아래 DO 구문은 수정 과제가 아닙니다.
DO $guard$
BEGIN
    IF current_database() <> 'day19_build_a' THEN
        RAISE EXCEPTION 'Wrong database: expected day19_build_a, got %', current_database();
    END IF;
END;
$guard$;
CREATE TABLE public.knowledge (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    -- BEGIN A-DDL-04
    -- 해설 A-DDL-04: knowledge의 title VARCHAR(80), content TEXT, category_id BIGINT를
    -- 각각 NOT NULL로 선언하세요. 각 줄에 쉼표를 붙입니다.
    title VARCHAR(80) NOT NULL,
    content TEXT NOT NULL,
    category_id BIGINT NOT NULL,
    -- END A-DDL-04
    -- BEGIN A-DDL-05
    -- 해설 A-DDL-05: NOT NULL과 길이 CHECK는 다른 규칙입니다. 빈 문자열은 NULL이 아니므로 길이 하한으로 막습니다.
    -- 제목 중복 금지나 공백 제거를 이 요구사항에 추가하지 않습니다.
    CONSTRAINT knowledge_title_length CHECK (char_length(title) BETWEEN 1 AND 80),
    CONSTRAINT knowledge_content_length CHECK (char_length(content) BETWEEN 1 AND 2000),
    -- END A-DDL-05
    -- BEGIN A-DDL-06
    -- 해설 A-DDL-06: FK는 실제 부모 존재를 검사합니다. category_id의 NOT NULL과 함께 필수 관계를 만들고
    -- RESTRICT는 참조 중인 부모 삭제를 막습니다. FK가 JOIN 결과를 자동으로 만들지는 않습니다.
    CONSTRAINT knowledge_category_fk FOREIGN KEY (category_id)
        REFERENCES public.categories(id) ON DELETE RESTRICT
    -- END A-DDL-06
);
COMMIT;
