-- Day18 | 실습 02: 지식 SELECT·조건·정렬 | PPT 14~20 | 35분
-- SQL 편집: VS Code / 실행: pgAdmin Query Tool (주 경로), psql (선택 경로)
-- @step은 실행 단위를 표시하는 주석입니다. SQL 명령이 아닙니다.
-- 한 @step 구간씩 선택 실행합니다. 오류 뒤 ROLLBACK은 반드시 별도 실행합니다.
-- __TODO_...__는 구현할 빈칸, __NEW_ID__/__A_ID__/__B_ID__/__C_ID__는 실제 실행 입력입니다.
-- 입력 ID는 RETURNING에서 읽어 해당 토큰을 실제 정수로 바꿉니다. 4·5·6으로 예측하지 않습니다.
-- 아직 남은 토큰 때문에 생긴 문법 오류는 의도한 제약 실패로 인정하지 않습니다.

-- @step E2_GUARD expect=00000 capture=- reconnect=false
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

-- @step E2_LIST expect=00000 capture=- reconnect=false
-- BEGIN TASK H02_01
-- 해설 H02_01
-- 필요한 열만 선택하고 ORDER BY id로 표시 순서를 명시합니다. 결과 한 행은 지식 한 건입니다.
SELECT id, title, category_id FROM public.knowledge ORDER BY id;
-- END TASK H02_01

-- @step E2_DETAIL expect=00000 capture=- reconnect=false
-- BEGIN TASK H02_02
-- 해설 H02_02
-- WHERE는 대상 행 조건입니다. 이 초기 데이터에서 id=2는 서버 실행입니다. 실제 상태가 다르면 먼저 대상 ID를 조회합니다.
SELECT id, title, content FROM public.knowledge
WHERE id = 2;
-- END TASK H02_02

-- @step E2_CATEGORY expect=00000 capture=- reconnect=false
-- BEGIN TASK H02_03
-- 해설 H02_03
-- 분류 1은 S0의 learning입니다. 실제 ID·행 수를 확인하며, 정렬 없는 결과의 순서를 가정하지 않습니다.
SELECT id, title FROM public.knowledge
WHERE category_id = 1
ORDER BY id;
-- END TASK H02_03

-- @step E2_EMPTY expect=00000 capture=- reconnect=false
SELECT id, title FROM public.knowledge WHERE id=-1;

-- @step E2_COMBINED expect=00000 capture=- reconnect=false
-- BEGIN TASK H02_04
-- 해설 H02_04
-- AND는 두 조건을 모두 만족하는 행만 남깁니다. S0에서는 id 1입니다. LIMIT만으로 행의 순서를 정하지 않습니다.
SELECT id, title FROM public.knowledge
WHERE category_id = 1 AND title ILIKE '%실습%'
ORDER BY id
LIMIT 1;
-- END TASK H02_04

-- @step E2_NULL expect=00000 capture=- reconnect=false
-- BEGIN TASK H02_05
-- 해설 H02_05
-- IS NULL만 TRUE가 되는 한 행입니다. label = NULL은 UNKNOWN이므로 동일한 조건이 아닙니다.
SELECT label, label IS NULL AS is_missing
FROM (VALUES (NULL::text), (''::text), ('안내')) AS s(label)
WHERE label IS NULL;
-- END TASK H02_05

-- @step E2_TIE expect=00000 capture=- reconnect=false
SELECT id,score FROM (VALUES (3,10),(1,10),(2,5)) AS s(id,score) ORDER BY score DESC,id;
