"""실습 06. 오류 분류 원리. 손계산 fixture를 사용하며 실제 YOLO 오류가 아닙니다."""
from pathlib import Path
import sys
import pandas as pd
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE.parent/"provided"))
from geometry import iou_matrix
from metrics import match_predictions
out=BASE/"outputs";out.mkdir(exist_ok=True)
p=pd.read_csv(BASE.parent/"data/boxes_fixture.csv").to_dict("records")
g=pd.read_csv(BASE.parent/"data/boxes_gt.csv").to_dict("records")
# >>> C06
# 요구: IoU .5 일대일 매칭을 호출하세요. 결과의 gt_index가 None이면 FP입니다.
pass  # TODO C06: 위 요구사항의 핵심 코드를 작성하세요.
# <<< C06
keys=["x1","y1","x2","y2"];rows=[]
for r in records:
    q=p[r["prediction_index"]]
    overlap=iou_matrix([[q[k] for k in keys]],[[t[k] for k in keys] for t in g])[0]
    j=int(overlap.argmax());same=q["class_id"]==g[j]["class_id"]
    reason="TP" if r["tp"] else ("Duplicate" if same and overlap[j]>=.5 else "Wrong_class" if not same and overlap[j]>=.5 else "Loose_box" if same and overlap[j]>=.1 else "Background_FP")
    rows.append(dict(prediction_index=r["prediction_index"],reason=reason,best_iou=float(overlap[j])))
pd.DataFrame(rows).to_csv(out/"fixture_errors.csv",index=False)
print(pd.DataFrame(rows).to_string(index=False));print(counts)
print("Miss는 매칭되지 않은 정답에서 따로 집계합니다.")
