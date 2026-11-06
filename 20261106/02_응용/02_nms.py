"""실습 02. 고전 NMS 원리 실험. YOLO26 기본 추론에 NMS가 있다고 가정하지 않습니다."""
from pathlib import Path
import torch
import pandas as pd
from torchvision.ops import box_iou, batched_nms
BASE=Path(__file__).resolve().parent
out=BASE/"outputs";out.mkdir(exist_ok=True)
p=pd.read_csv(BASE/"data/boxes_fixture.csv");g=pd.read_csv(BASE/"data/boxes_gt.csv")
boxes=torch.tensor(p[["x1","y1","x2","y2"]].to_numpy(),dtype=torch.float32)
scores=torch.tensor(p.confidence.to_numpy(),dtype=torch.float32)
classes=torch.tensor(p.class_id.to_numpy(),dtype=torch.int64)
gb=torch.tensor(g[["x1","y1","x2","y2"]].to_numpy(),dtype=torch.float32)
rows=[]
for conf,nms_iou in [(0.25,0.5),(0.5,0.5),(0.25,0.95)]:
    ids=torch.where(scores>=conf)[0]
    # >>> A02
    # 요구: 같은 클래스끼리만 중복을 제거하는 batched_nms를 적용하세요.
    # 반환 index는 ids로 줄인 배열 기준이므로 다시 원본 index로 바꿉니다.
    pass  # TODO A02: 위 요구사항의 핵심 코드를 작성하세요.
    # <<< A02
    used=set();tp=0
    for i in keep.tolist():
        ovs=box_iou(boxes[[i]],gb)[0]
        eligible=[j for j in range(len(g)) if int(classes[i])==int(g.iloc[j].class_id) and j not in used]
        for j in sorted(eligible,key=lambda j:-float(ovs[j])):
            if ovs[j]>=0.5:used.add(j);tp+=1;break
    n=len(keep);fp=n-tp;fn=len(g)-tp
    rows.append(dict(conf=conf,nms_iou=nms_iou,kept=n,tp=tp,fp=fp,fn=fn,precision=tp/n if n else 0,recall=tp/len(g)))
r=pd.DataFrame(rows);r.to_csv(out/"nms_comparison.csv",index=False);print(r.round(4).to_string(index=False))
