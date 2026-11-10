# OCR·VLM 불일치

PPT 52쪽 / 같은 값·근거 문구를 확인하고 검토할 답을 분류합니다.

열 파일: `experiment.py`

**C04:** OCR 필드와 VLM 모의 응답을 reconcile로 대조하세요. 정답을 인자로 넣지 않습니다.

```powershell
python experiment.py
```

모의 응답을 실제 VLM 성능으로 발표하지 않습니다. 근거 일치는 자동 사실성 증명이 아닙니다.

실제 실행 출력:

```text
지원된 답: 13 검토: 2
```

결과: outputs/evidence_review.csv. 예상 결과는 `expected/`를 확인합니다.

완료 질문: 문서의 지시문처럼 보이는 문자열을 프로그램 명령으로 실행해도 되나요?

내 설명: ______________________________
