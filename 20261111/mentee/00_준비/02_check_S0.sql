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
-- 읽기 전용. false가 나와도 초기화하지 말고, 현재 작업 상태부터 확인합니다.
SELECT current_database() AS database_name;
SELECT id, name FROM public.categories ORDER BY id;
SELECT id, title, content, category_id FROM public.knowledge ORDER BY id;
SELECT c.name AS category, COUNT(k.id) AS knowledge_count
FROM public.categories AS c
LEFT JOIN public.knowledge AS k ON k.category_id=c.id
GROUP BY c.id,c.name ORDER BY c.id;
SELECT COUNT(*) AS knowledge_count,
       SUM(char_length(content)) AS total_chars,
       MIN(char_length(content)) AS min_chars,
       MAX(char_length(content)) AS max_chars
FROM public.knowledge;
-- 새로 준비한 S0: 3건 / 64자 / 20자 / 24자
-- 7교시 COMMIT 이후(S1)에는 길이 64를 정답으로 요구하지 않습니다.
