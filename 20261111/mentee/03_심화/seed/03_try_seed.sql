-- 같은 Query Tool 연결을 유지한 채 실행합니다.

-- @step E3_SEED expect=00000 capture=- reconnect=false
INSERT INTO public.categories_try VALUES (1,'연습');
INSERT INTO public.knowledge_try VALUES (1,'안내',1);
