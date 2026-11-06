"""실습 02. 제공한 원리 모듈로 여러 IoU에서 AP를 비교합니다."""
from pathlib import Path
import sys
import pandas as pd
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE.parent/"provided"))
from metrics import evaluate
out=BASE/"outputs";out.mkdir(exist_ok=True)
p=pd.read_csv(BASE.parent/"data/boxes_fixture.csv").to_dict("records")
g=pd.read_csv(BASE.parent/"data/boxes_gt.csv").to_dict("records")
# >>> C02
# 요구: 세 클래스 모두를 .50~.95 IoU에서 평가하는 표를 만드세요.
pass  # TODO C02: 위 요구사항의 핵심 코드를 작성하세요.
# <<< C02
r.to_csv(out/"ap_by_class_iou.csv",index=False)
print("educational_AP101 mAP50:",round(r.loc[r.iou_threshold==.5,"ap"].mean(),4))
print("educational_AP101 mAP50-95:",round(r.ap.mean(),4))
print(r.groupby("class_id").ap.mean().round(4).to_string())
