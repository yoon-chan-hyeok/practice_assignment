# 실습을 위한 환경 설정
1. 아래 링크를 통해 postgresql 18.6.x를 받아주세요  
https://www.enterprisedb.com/downloads/postgres-postgresql-downloads  
2. 설치를 진행합니다.  
password는 일단 기억하기 쉬운걸로 설정해둡니다. (pw까먹으면 postgresql 다시 설치하셔야해요)  
3. powershell에서 아래 명령어를 통해 잘 설치됐는지 확인  
Get-Service *postgres*  
아래처럼 뜨면 잘 설치된거에요.  

Status   Name               DisplayName
------   ----               -----------
Running  postgresql-x64-18  postgresql-x64-18  

4. powershelldptj 아래명령어를 통해 path 설정  
$psql = Get-ChildItem "C:\Program Files\PostgreSQL" `
    -Filter psql.exe -Recurse -File |
    Select-Object -First 1

if (-not $psql) {
    throw "psql.exe를 찾지 못했습니다."
}

$env:PATH = "$($psql.DirectoryName);$env:PATH"

psql --version




아래처럼 나오면 잘된거에요.
psql (PostgreSQL) 18.6  

5. 아래경로를 통해 dbvear을 설치해주세요  
https://dbeaver.io/download/  

  
  
  
# 제공 준비 SQL — TODO 없음

PPT 부록 A01~A05의 완성된 두 테이블과 가상 초기 데이터입니다.
2교시에 곧바로 SELECT할 수 있게 제공하는 시작점이며, 3교시 _try DDL 과제의 정답을 제출하는 파일이 아닙니다.

| 순서 | 어디에서 | 파일 | 결과 |
|---|---|---|---|
| 0 | postgres DB, 자동 커밋 | 00_create_database.sql | 새 knowledge_lab DB. 이미 있으면 생략/확인 |
| 1 | knowledge_lab DB | 01_prepare_S0.sql | 두 표와 분류 3·지식 3건, 트랜잭션으로 준비 |
| 2 | 같은 DB | 02_check_S0.sql | 목록·분류별 2/1/0·길이 64 확인 |
| 3 | 같은 DB, 필요 시 | 03_inspect_schema.sql | 실제 열·키·제약·인덱스 확인 |

01은 새 빈 표를 만드는 작업입니다. 기존 categories/knowledge가 하나라도 있으면 중단하도록 작성했습니다.
IF NOT EXISTS로 다른 정의를 숨기거나 ON CONFLICT로 잘못된 준비를 덮지 않습니다.
오류가 나면 ROLLBACK만 실행하고 원인을 확인합니다. 준비 성공 후 01을 다시 실행하지 않습니다.
복구·재접속·다음 교시 시작은 Seed 재실행을 의미하지 않습니다.

DDL·Seed 모두 UTF-8입니다. 준비 단계의 DO 블록은 잘못된 DB와 중복 준비를 막는 제공 안전 코드이며
초급자가 직접 작성하거나 문법을 외울 대상이 아닙니다.
