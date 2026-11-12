-- 제공 안전장치: 아래 DO 구문은 수정 과제가 아닙니다.
DO $guard$
BEGIN
    IF current_database() <> 'day19_build_h' THEN
        RAISE EXCEPTION 'Wrong database: expected day19_build_h, got %', current_database();
    END IF;
END;
$guard$;
-- 구축 직후 비어 있는 두 테이블에서 수행하는 제공 점검입니다.
-- 임시 데이터는 ROLLBACK되어 남지 않습니다. 시퀀스 번호는 증가할 수 있습니다.
BEGIN;
INSERT INTO public.categories(name) VALUES ('__build_check__') RETURNING id,name;
INSERT INTO public.knowledge(title,content,category_id)
SELECT '구축 확인','가상의 점검 내용입니다.',id
FROM public.categories WHERE name='__build_check__'
RETURNING id,title;
SELECT k.title,c.name AS category FROM public.knowledge k
JOIN public.categories c ON c.id=k.category_id WHERE c.name='__build_check__';
ROLLBACK;
SELECT COUNT(*) AS knowledge_count FROM public.knowledge;
-- 기대: 생성 각각 1행, JOIN 1행, 취소 후 knowledge_count=0 (빈 구축 DB 기준).
