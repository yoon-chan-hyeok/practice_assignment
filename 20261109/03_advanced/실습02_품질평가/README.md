# 문자·필드 품질

PPT 29쪽 / CER과 필드 정확도를 분리해서 기록합니다.

열 파일: `experiment.py`

**C02:** 제공된 cer 함수에 정답 문자열을 첫째 인자, OCR 문자열을 둘째 인자로 전달하세요.

```powershell
python experiment.py
```

CER의 공백·유니코드·빈 정답 정책은 evaluate.py에 명시되어 있습니다.

실제 실행 출력:

```text
document_id     cer  field_exact
      doc01 0.00658            3
      doc02 0.00667            3
      doc03 0.00633            3
      doc04 0.00000            3
      doc05 0.00676            3
```

결과: outputs/quality.csv. 예상 결과는 `expected/`를 확인합니다.

완료 질문: 필드 3개가 모두 맞아도 CER이 0이 아닐 수 있는 이유는?

내 설명: ______________________________
