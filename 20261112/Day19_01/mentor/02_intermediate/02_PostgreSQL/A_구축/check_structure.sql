-- 제공 안전장치: 아래 DO 구문은 수정 과제가 아닙니다.
DO $guard$
BEGIN
    IF current_database() <> 'day19_build_a' THEN
        RAISE EXCEPTION 'Wrong database: expected day19_build_a, got %', current_database();
    END IF;
END;
$guard$;
-- 각 결과를 스키마명세서와 비교합니다. column_default의 내부 시퀀스명은 채점하지 않습니다.
SELECT table_name, column_name, data_type, character_maximum_length,
       is_nullable, is_identity, identity_generation
FROM information_schema.columns
WHERE table_schema='public' AND table_name IN ('categories','knowledge')
ORDER BY table_name, ordinal_position;

SELECT conrelid::regclass AS table_name, contype, conname,
       pg_get_constraintdef(oid) AS definition
FROM pg_constraint
WHERE conrelid IN ('public.categories'::regclass, 'public.knowledge'::regclass)
ORDER BY conrelid::regclass::text, contype, conname;
-- PostgreSQL 버전에 따라 NOT NULL이 catalog 결과에 더 표시될 수 있습니다.
-- PK/UQ의 자동 이름이나 CHECK 표현의 괄호 개수 대신 실제 열·규칙·FK 삭제 정책을 확인합니다.
