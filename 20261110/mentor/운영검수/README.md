# 강사용 운영 검수

검수결과.md를 먼저 읽으세요. JSON·TXT 로그는 제작 당시 실제 관찰 결과입니다.
학생에게 이 폴더의 도구 실행을 요구하지 않습니다.

재검사: 강사용 루트에서 requirements-test.txt 설치 후 다음 명령을 실행합니다.

```powershell
python 운영검수/verify_materials.py
```

통합본의 형제 수강생용 폴더까지 정답 대입 검사하려면 --include-student를 붙입니다.
기존 검수 JSON을 덮어쓰지 않고 verification_local.json에 새 결과를 저장합니다.
모든 API 계약 검사는 임시 데이터 파일을 사용합니다. 실제 서버 재시작은 각 프로젝트 안내대로 별도 확인합니다.
