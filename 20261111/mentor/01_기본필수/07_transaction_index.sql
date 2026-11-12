-- Day18 | 실습 07: 취소·확정·인덱스·실행계획 | PPT 48~54, 76 | 30분
-- SQL 편집: VS Code / 실행: pgAdmin Query Tool (주 경로), psql (선택 경로)
-- @step은 실행 단위를 표시하는 주석입니다. SQL 명령이 아닙니다.
-- 한 @step 구간씩 선택 실행합니다. 오류 뒤 ROLLBACK은 반드시 별도 실행합니다.
-- __TODO_...__는 구현할 빈칸, __NEW_ID__/__A_ID__/__B_ID__/__C_ID__는 실제 실행 입력입니다.
-- 입력 ID는 RETURNING에서 읽어 해당 토큰을 실제 정수로 바꿉니다. 4·5·6으로 예측하지 않습니다.
-- 아직 남은 토큰 때문에 생긴 문법 오류는 의도한 제약 실패로 인정하지 않습니다.

-- @step E7_GUARD expect=00000 capture=- reconnect=false
-- 제공된 안전 확인입니다. 이 블록은 TODO가 아닙니다.
-- 개인 수업용 DB에서만 실행합니다. 이름만 맞다고 운영 DB가 안전해지는 것은 아닙니다.
DO $guard$
BEGIN
  IF current_database() !~ '^knowledge_lab(_[a-z0-9_]+)?$' THEN
    RAISE EXCEPTION '개인 knowledge_lab DB에 다시 접속하세요. 현재 DB: %', current_database();
  END IF;
END;
$guard$;
SET search_path TO public;

-- @step E7_BEFORE expect=00000 capture=- reconnect=false
SELECT id,content FROM public.knowledge WHERE id=2;

-- @step E7_CANCEL_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step E7_TEMP expect=00000 capture=- reconnect=false
UPDATE public.knowledge SET content='취소할 임시 안내입니다.' WHERE id=2 RETURNING id,content;

-- @step E7_CANCEL expect=00000 capture=- reconnect=false
-- BEGIN TASK B07_01
-- 해설 B07_01
-- ROLLBACK은 바로 앞 BEGIN 이후 변경을 취소합니다. 초기 Seed로 항상 돌아가는 초기화 명령이 아닙니다.
ROLLBACK;
-- END TASK B07_01

-- @step E7_CANCEL_READ expect=00000 capture=- reconnect=false
SELECT id,content FROM public.knowledge WHERE id=2;

-- @step E7_SAVE_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step E7_SAVE expect=00000 capture=- reconnect=false
UPDATE public.knowledge SET content='실행 전에 가상환경을 확인합니다.' WHERE id=2 RETURNING id,content;

-- @step E7_COMMIT expect=00000 capture=- reconnect=false
-- BEGIN TASK B07_02
-- 해설 B07_02
-- COMMIT으로 변경을 확정합니다. 이후 새 연결에서 조회하는 것은 서버 장애 시험이 아닙니다. S1에서 시작할 일일프로젝트는 이 값을 기존 데이터로 보존합니다.
COMMIT;
-- END TASK B07_02

-- @step E7_RECONNECT expect=00000 capture=- reconnect=true
SELECT current_database() AS database_name;
SELECT id,content FROM public.knowledge WHERE id=2;

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
