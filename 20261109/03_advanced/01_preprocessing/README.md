# 전처리 후보의 CER 비교

PPT 19쪽 / 회전·그림자·저해상도 자료의 실제 OCR 기록을 비교합니다.

열 파일: `experiment.py`

**C01:** 각 case에서 CER이 가장 낮은 후보를 선택하세요. 동점은 candidate 이름순으로 고정합니다.

```powershell
python experiment.py
```

기록된 9개 OCR 결과를 재평가합니다. 추론을 다시 실행하지 않으므로 시간은 null입니다.

실제 실행 출력:

```text
case candidate    cer
 lowres corrected 0.0190
rotated corrected 0.0063
 shadow corrected 0.0063
```

결과: outputs/candidates.csv, selected.csv. 예상 결과는 `expected/`를 확인합니다.

완료 질문: 개발 문서에서 선택한 최저 CER을 독립 test 성능이라고 할 수 있나요?

내 설명: ______________________________
