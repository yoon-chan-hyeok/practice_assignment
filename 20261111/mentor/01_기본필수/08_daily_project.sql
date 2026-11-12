-- Day18 | 실습 08: 나만의 AI 도움말 지식 DB | PPT 58~67 | 40분
-- SQL 편집: VS Code / 실행: pgAdmin Query Tool (주 경로), psql (선택 경로)
-- @step은 실행 단위를 표시하는 주석입니다. SQL 명령이 아닙니다.
-- 한 @step 구간씩 선택 실행합니다. 오류 뒤 ROLLBACK은 반드시 별도 실행합니다.
-- __TODO_...__는 구현할 빈칸, __NEW_ID__/__A_ID__/__B_ID__/__C_ID__는 실제 실행 입력입니다.
-- 입력 ID는 RETURNING에서 읽어 해당 토큰을 실제 정수로 바꿉니다. 4·5·6으로 예측하지 않습니다.
-- 아직 남은 토큰 때문에 생긴 문법 오류는 의도한 제약 실패로 인정하지 않습니다.

-- @step E8_GUARD expect=00000 capture=- reconnect=false
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
-- 이 파일은 앞서 사용한 DB를 이어 씁니다. prepare_S0.sql을 다시 실행하지 않습니다.
-- 시작 N과 기존 전체 지식을 reports/daily_note.md에 기록/내보내기 합니다.
-- A·B·C 생성은 각각 1번만 실행합니다. 실수로 중복 생성하면 실제 ID를 확인하고 강사와 정리하세요.
-- __A_ID__, __B_ID__, __C_ID__는 실제 RETURNING 값으로 모두 바꾼 뒤 사용합니다.
-- 기본필수도 자신의 주제에 맞게 세 제목·본문을 작성합니다. 제공 예문은 가상 예시입니다.

-- @step D8_BASELINE expect=00000 capture=- reconnect=false
SELECT current_database() AS database_name;
SELECT COUNT(*) AS baseline_n FROM public.knowledge;
SELECT id, title, content, category_id FROM public.knowledge ORDER BY id;
SELECT id,name FROM public.categories ORDER BY id;

-- @step D8_CREATE_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step D8_CREATE_A expect=00000 capture=a_ reconnect=false
-- BEGIN TASK B08_01
-- 해설 B08_01
-- 이 가상 안내는 강사 시연 예시이지 유일한 정답이 아닙니다. A/B/C는 역할 이름이며 테이블의 새 열이 아닙니다. RETURNING을 읽고 실제 ID로 추적합니다.
INSERT INTO public.knowledge(title,content,category_id)
VALUES ('학습 자료 보관', '가상의 학습 자료는 개인 폴더에 보관합니다.', 1)
RETURNING id,title,content,category_id;
-- END TASK B08_01

-- @step D8_CREATE_B expect=00000 capture=b_ reconnect=false
-- 개인 주제에 맞게 제목·본문을 바꾸세요. B는 나중에 본문을 수정할 대상입니다.
INSERT INTO public.knowledge(title,content,category_id)
VALUES ('실습 결과 기록', '가상의 결과는 개인 폴더에 남깁니다.', 2)
RETURNING id,title,content,category_id;

-- @step D8_CREATE_C expect=00000 capture=c_ reconnect=false
-- 개인 주제에 맞게 제목·본문을 바꾸세요. C는 나중에 삭제할 대상입니다.
INSERT INTO public.knowledge(title,content,category_id)
VALUES ('폐기할 임시 안내', '가상의 임시 안내는 확인 후 제거합니다.', 1)
RETURNING id,title,content,category_id;

-- @step D8_CREATE_COMMIT expect=00000 capture=- reconnect=false
COMMIT;

-- @step D8_LIST expect=00000 capture=- reconnect=false
SELECT k.id, k.title, k.content, c.name AS category
FROM public.knowledge AS k
JOIN public.categories AS c ON c.id = k.category_id
ORDER BY k.id;

SELECT COUNT(*) AS after_create_count FROM public.knowledge;

-- @step D8_B_ORIGINAL expect=00000 capture=- reconnect=false
SELECT id,title,content,category_id FROM public.knowledge WHERE id=__B_ID__;

-- @step D8_B_CANCEL_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step D8_B_TEMP expect=00000 capture=- reconnect=false
UPDATE public.knowledge SET content='취소할 임시 프로젝트 본문입니다.' WHERE id=__B_ID__ RETURNING id,content;

-- @step D8_B_CANCEL expect=00000 capture=- reconnect=false
ROLLBACK;

-- @step D8_B_RESTORED expect=00000 capture=- reconnect=false
SELECT id,content FROM public.knowledge WHERE id=__B_ID__;

-- @step D8_B_SAVE_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step D8_B_SAVE expect=00000 capture=- reconnect=false
-- 원문과 다른 자신의 수정 내용을 적어도 됩니다.
UPDATE public.knowledge SET content='결과에는 실행 명령과 실제 SQL 결과를 함께 적습니다.'
WHERE id=__B_ID__ RETURNING id,content;

-- @step D8_B_COMMIT expect=00000 capture=- reconnect=false
-- BEGIN TASK B08_02
-- 해설 B08_02
-- 취소 실험과 확정 실험은 서로 다른 트랜잭션입니다. 변경 대상 B만 바뀌고 기존 행·A는 그대로여야 합니다.
COMMIT;
-- END TASK B08_02

-- @step D8_B_RECONNECT expect=00000 capture=- reconnect=true
SELECT current_database() AS database_name;
SELECT id,content FROM public.knowledge WHERE id=__B_ID__;

-- @step D8_ERRORS_BEFORE expect=00000 capture=- reconnect=false
SELECT id, title, content, category_id FROM public.knowledge ORDER BY id;
SELECT id FROM public.categories WHERE id=-1;

-- @step D8_CHECK_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step D8_CHECK_FAIL expect=23514 capture=- reconnect=false
INSERT INTO public.knowledge(title,content,category_id) VALUES ('실패 확인','',1);

-- @step D8_CHECK_CANCEL expect=00000 capture=- reconnect=false
ROLLBACK;

-- @step D8_FK_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step D8_FK_FAIL expect=23503 capture=- reconnect=false
INSERT INTO public.knowledge(title,content,category_id) VALUES ('실패 확인','정상 본문',-1);

-- @step D8_FK_CANCEL expect=00000 capture=- reconnect=false
ROLLBACK;

-- @step D8_ERRORS_AFTER expect=00000 capture=- reconnect=false
SELECT id, title, content, category_id FROM public.knowledge ORDER BY id;

-- @step D8_C_BEFORE expect=00000 capture=- reconnect=false
SELECT id,title FROM public.knowledge WHERE id=__C_ID__;

-- @step D8_C_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step D8_C_DELETE expect=00000 capture=- reconnect=false
-- BEGIN TASK B08_03
-- 해설 B08_03
-- C 한 행만 삭제하고 COMMIT합니다. 같은 제목의 다른 지식이 있을 수 있으므로 실제 ID를 조건으로 사용합니다.
DELETE FROM public.knowledge
WHERE id = __C_ID__
RETURNING id,title;
-- END TASK B08_03

-- @step D8_C_COMMIT expect=00000 capture=- reconnect=false
COMMIT;

-- @step D8_FINAL_RECONNECT expect=00000 capture=- reconnect=true
SELECT current_database() AS database_name;
SELECT id,title,content,category_id FROM public.knowledge WHERE id IN (__A_ID__,__B_ID__) ORDER BY id;
SELECT id,title FROM public.knowledge WHERE id=__C_ID__;
SELECT COUNT(*) AS final_count FROM public.knowledge;

-- @step D8_GROUP expect=00000 capture=- reconnect=false
-- BEGIN TASK B08_04
-- 해설 B08_04
-- 집계는 전체 지식과 같은 범위를 사용해야 합니다. 프로젝트 A·B만 따로 센 결과를 전체 N+2와 비교하지 않습니다.
SELECT c.name, COUNT(k.id) AS knowledge_count
FROM public.categories c
LEFT JOIN public.knowledge k ON k.category_id=c.id
GROUP BY c.id,c.name ORDER BY c.id;
-- END TASK B08_04

-- @step D8_EXISTING expect=00000 capture=- reconnect=false
SELECT id, title, content, category_id FROM public.knowledge ORDER BY id;
