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
SELECT table_name,column_name,data_type,character_maximum_length,
       is_nullable,is_identity
FROM information_schema.columns
WHERE table_schema='public' AND table_name IN ('categories','knowledge')
ORDER BY table_name,ordinal_position;
SELECT conrelid::regclass AS table_name,conname,
       pg_get_constraintdef(oid) AS definition
FROM pg_constraint
WHERE conrelid IN ('public.categories'::regclass,'public.knowledge'::regclass)
ORDER BY conrelid::regclass::text,conname;
SELECT tablename,indexname,indexdef FROM pg_indexes
WHERE schemaname='public' AND tablename IN ('categories','knowledge')
ORDER BY tablename,indexname;
