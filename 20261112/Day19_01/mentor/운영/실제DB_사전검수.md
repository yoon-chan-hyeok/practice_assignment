# 실제 PostgreSQL 사전검수

**제작 환경에는 PostgreSQL 서버·psql이 없고 다운로드 네트워크도 사용할 수 없어 실제 PostgreSQL 실행은 미검증입니다.**
SQL 예상 결과는 기준 데이터의 논리 대조이며, 실제 DB 로그를 만들어 넣지 않았습니다.
수업 전에 강사 환경의 PostgreSQL 18에서 아래 수동 또는 선택 자동 경로로 확인하세요.

## 수동 경로 (추가 Python 패키지 불필요)
1. 강사용 선택 수준의 02_PostgreSQL/00_접속준비.sql 안내대로 구축용과 CRUD용 전용 개인 DB를 생성합니다.
2. 스키마명세서에 지정된 A_구축 SQL을 부모부터 실행하고 check_structure.sql·check_insert.sql을 대조합니다.
3. 다른 전용 DB에 B_CRUD/00_ready_database.sql을 한 번 실행합니다. 기존 knowledge_lab은 건드리지 않습니다.
4. R 조회 문제들의 열·값·순서를 예상 CSV/표와 비교합니다.
5. C01 INSERT의 RETURNING에서 실제 ID를 기록합니다. U01·U02·D01의 __NEW_ID__를 바꿉니다.
6. BEGIN → 변경문 RETURNING → 결과 확인 → 종료문 → 후속 SELECT를 각각 선택 실행합니다.
7. errors.sql의 실패 CASE와 RECOVER를 분리 실행합니다. 기대 SQLSTATE와 취소 후 기존 세 행 보존을 확인합니다.
8. 심화는 추가 인덱스와 T01 복합 취소도 확인합니다. 특정 Scan·시간이나 연속 ID는 필수 정답이 아닙니다.

## 선택 자동 경로 (강사 전용)
운영 폴더에서 실행합니다. 학생용 환경에는 이 의존성이 필요하지 않습니다.

```powershell
python -m pip install -r requirements-verify.txt
python verify_files.py
python verify_postgres.py --allow-test-db-creation --host localhost --port 5432 --user postgres --ask-password
```

실제 계정·포트를 사용하세요. 비밀번호는 화면에 보이지 않게 입력되며 명령 인자나 보고서에 기록하지 않습니다.
도구는 무작위 이름의 `day19_check_*` 새 DB 6개를 만듭니다. 이미 같은 이름이 있으면 실행을 거부합니다.
강사용 SQL을 읽어 접속대상 보호문만 새 검수 DB 이름으로 바꾸고, 명세의 쿼리·변경·실패 결과를 검사합니다.
**기존 DB의 DROP·TRUNCATE를 하지 않으며 자동 정리도 하지 않습니다.** 생성된 DB 목록을 결과 JSON에 남기므로 필요한 검수 DB만 나중에 관리자가 정리합니다.
권한이 없으면 개인 학습 서버에서 수동 경로로 검수하세요. 보안 정책 변경이나 운영 계정 사용을 요구하지 않습니다.
이 도구 자체도 PostgreSQL 접속 구간은 제작 환경에서 실행하지 못했습니다. 문법 검사·CASE 추출 검사와 실제 DB 실행 검증을 구분합니다.
