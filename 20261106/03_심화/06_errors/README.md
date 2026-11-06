# 실습 06_errors · 오류 유형 원리
PPT 75쪽 / 완성할 곳: C06

이 폴더에서 `python main.py`를 실행합니다. 입력은 상위 `data/`, 결과는 이 폴더의 `outputs/`입니다.

**C06**: 요구: IoU .5 일대일 매칭을 호출하세요. 결과의 gt_index가 None이면 FP입니다.

실행 확인 출력:
```text
prediction_index        reason  best_iou
                0            TP  0.902500
                1     Duplicate  0.816229
                2            TP  1.000000
                3 Background_FP  0.000000
{'tp': 2, 'fp': 2, 'fn': 1}
Miss는 매칭되지 않은 정답에서 따로 집계합니다.
```

완료: TODO·실행·결과 저장·설명 2문장. 관찰한 오류와 원인 가설을 구분하세요.

내 설명: __________________
