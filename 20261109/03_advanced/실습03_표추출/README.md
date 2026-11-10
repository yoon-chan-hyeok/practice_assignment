# 고정 표와 합계

PPT 39쪽 / 행별 수량×단가와 전체 합계를 확인합니다.

열 파일: `experiment.py`

**C03:** 원문에서 3개 품목 행을 추출하세요. 정답의 items를 복사하지 않습니다.

```powershell
python experiment.py
```

extract_items는 고정 4열만 지원하는 수업용 규칙입니다. schema_version을 함께 기록합니다.

실제 실행 출력:

```text
품목 수: 3 총금액: 33000 검토 이유: []
```

결과: outputs/invoice.json. 예상 결과는 `expected/`를 확인합니다.

완료 질문: 복잡한 병합 셀 표에도 이 정규표현식만 적용해도 될까요?

내 설명: ______________________________
