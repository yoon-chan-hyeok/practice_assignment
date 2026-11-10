# OCR·모의 VLM·Hybrid 평가

PPT 62쪽 / 전체 분모와 답변 커버리지·검토 수를 함께 보고합니다.

열 파일: `experiment.py`

**C05:** 정답 일치·응답 유무·검토 유무를 각각 기록하세요. 보류(None)는 이번 정답과 일치하지 않습니다. 추론시간은 None입니다.

```powershell
python experiment.py
```

사람 검토 결과를 자동 정답으로 대체하지 않습니다. mode별 성능 비교가 아닌 평가 구조 연습입니다.

실제 실행 출력:

```text
exact  answered  review
mode                                  
hybrid_review     13        13       2
ocr_recorded      15        15       0
vlm_mock          14        15       0
각 mode 분모 15. 답변 보류를 정답으로 세지 않습니다. 속도 비교 없음.
```

결과: outputs/field_evaluation.csv. 예상 결과는 `expected/`를 확인합니다.

완료 질문: 보류를 제외하고 정확도만 높게 보이면 어떤 문제가 생길까요?

내 설명: ______________________________
