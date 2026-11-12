-- 제공 안전장치: 아래 DO 구문은 수정 과제가 아닙니다.
DO $guard$
BEGIN
    IF current_database() <> 'day19_crud_h' THEN
        RAISE EXCEPTION 'Wrong database: expected day19_crud_h, got %', current_database();
    END IF;
END;
$guard$;
-- 제공 확인: 특정 계획이나 속도 수치를 정답으로 요구하지 않습니다. SELECT만 사용합니다.
EXPLAIN SELECT id,title FROM public.knowledge WHERE category_id=1 ORDER BY id;
SELECT indexname, indexdef FROM pg_indexes
WHERE schemaname='public' AND tablename='knowledge' ORDER BY indexname;
