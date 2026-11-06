"""실습 02. 손으로 정한 예측 4개를 정답 3개와 비교합니다. YOLO 결과가 아닙니다."""
from pathlib import Path
import numpy as np
import pandas as pd
BASE = Path(__file__).resolve().parent
pred = pd.read_csv(BASE / "data/boxes_fixture.csv")  # confidence 내림차순 예시
truth = pd.read_csv(BASE / "data/boxes_gt.csv")
used = set()  # 하나의 정답은 한 번만 TP로 연결합니다.
rows = []
for p in pred.itertuples():
    overlaps = []
    for g in truth.itertuples():
        width = max(0, min(p.x2, g.x2) - max(p.x1, g.x1))
        height = max(0, min(p.y2, g.y2) - max(p.y1, g.y1))
        intersection = width * height
        union = (p.x2-p.x1)*(p.y2-p.y1) + (g.x2-g.x1)*(g.y2-g.y1) - intersection
        # >>> B02
        # 요구: intersection을 union으로 나누어 iou를 계산하세요.
        # 이 실습의 데이터는 모두 양의 면적이므로 union은 0이 아닙니다.
        pass  # TODO B02: 위 요구사항의 핵심 코드를 작성하세요.
        # <<< B02
        overlaps.append(iou)
    matched = False
    for j in np.argsort(-np.asarray(overlaps)):
        if truth.iloc[j].class_id != p.class_id or j in used:
            continue
        # >>> B03
        # 요구: 같은 클래스의 미사용 정답에 IoU>=0.5이면 연결하고 used에 기록하세요.
        pass  # TODO B03: 위 요구사항의 핵심 코드를 작성하세요.
        # <<< B03
    rows.append([p.class_id, p.confidence, round(max(overlaps), 4), "TP" if matched else "FP"])
table = pd.DataFrame(rows, columns=["class", "confidence", "max_iou", "result"])
print(table.to_string(index=False))
tp = len(used); fp = len(pred)-tp; fn = len(truth)-tp
print("TP/FP/FN:", tp, fp, fn)
print("Precision/Recall:", round(tp/len(pred), 4), round(tp/len(truth), 4))
table.to_csv(BASE / "p02_matching.csv", index=False, encoding="utf-8-sig")
