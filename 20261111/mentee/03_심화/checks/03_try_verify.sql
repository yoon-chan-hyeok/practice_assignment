-- 앞 두 파일과 같은 연결. 마지막 ROLLBACK을 빠뜨리지 않습니다.

-- @step E3_READ expect=00000 capture=- reconnect=false
SELECT * FROM public.knowledge_try ORDER BY id;

-- @step E3_CANCEL expect=00000 capture=- reconnect=false
ROLLBACK;

-- @step E3_GONE expect=00000 capture=- reconnect=false
SELECT to_regclass('public.categories_try') IS NULL AS parent_gone,
       to_regclass('public.knowledge_try') IS NULL AS child_gone;
