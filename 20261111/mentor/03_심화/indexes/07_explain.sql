-- 실제 SELECT만 측정합니다. cost는 밀리초가 아닙니다.

-- @step E7_INDEX_INSPECT expect=00000 capture=- reconnect=false
SELECT indexname,indexdef FROM pg_indexes WHERE schemaname='public' AND tablename='knowledge' ORDER BY indexname;

-- @step E7_PLAN_BEFORE expect=00000 capture=- reconnect=false
EXPLAIN SELECT id,title FROM public.knowledge WHERE category_id=1;

-- 같은 이름이 이미 있으면 정의를 확인하고 CREATE 구간을 건너뜁니다.

-- @step E7_INDEX_CREATE expect=00000 capture=- reconnect=false
CREATE INDEX idx_knowledge_category_id ON public.knowledge(category_id);

-- @step E7_PLAN_AFTER expect=00000 capture=- reconnect=false
EXPLAIN (ANALYZE, BUFFERS) SELECT id,title FROM public.knowledge WHERE category_id=1;

-- @step E7_FINAL expect=00000 capture=- reconnect=false
SELECT id, title, content, category_id FROM public.knowledge ORDER BY id;
