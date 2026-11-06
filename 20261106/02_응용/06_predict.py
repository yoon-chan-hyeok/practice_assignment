"""실습 06. 동일 모델·입력에서 conf만 바꾸고 고정 IoU=.5 매칭을 비교합니다."""
from pathlib import Path
import torch,cv2
import pandas as pd
from torchvision.ops import box_iou
from ultralytics import YOLO
BASE=Path(__file__).resolve().parent
out=BASE/"outputs";out.mkdir(exist_ok=True)
torch.set_num_threads(1);model=YOLO(str(BASE/"data/demo.pt"));records=[]
for conf in [.15,.25,.50]:
    tp=fp=fn=0
    # >>> A06
    # 요구: 같은 val 이미지 폴더를 현재 conf 값으로 추론하세요. stream=True를 사용합니다.
    pass  # TODO A06: 위 요구사항의 핵심 코드를 작성하세요.
    # <<< A06
    for result in results:
        h,w=result.orig_shape;gt=[];classes=[]
        for line in (BASE/"data/labels/val"/(Path(result.path).stem+".txt")).read_text().splitlines():
            cls,cx,cy,bw,bh=map(float,line.split());gt.append([(cx-bw/2)*w,(cy-bh/2)*h,(cx+bw/2)*w,(cy+bh/2)*h]);classes.append(int(cls))
        used=set();preds=result.boxes.cpu();matched=0
        for i in torch.argsort(preds.conf,descending=True,stable=True).tolist():
            if not gt:continue
            ovs=box_iou(preds.xyxy[[i]],torch.tensor(gt,dtype=torch.float32))[0]
            for j in sorted([j for j in range(len(gt)) if classes[j]==int(preds.cls[i]) and j not in used],key=lambda j:-float(ovs[j])):
                if ovs[j]>=.5:used.add(j);matched+=1;break
        tp+=matched;fp+=len(preds)-matched;fn+=len(gt)-matched
    records.append(dict(conf=conf,tp=tp,fp=fp,fn=fn,precision=tp/(tp+fp) if tp+fp else 0,recall=tp/(tp+fn) if tp+fn else 0))
r=pd.DataFrame(records);r.to_csv(out/"confidence_comparison.csv",index=False);print(r.to_string(index=False))
