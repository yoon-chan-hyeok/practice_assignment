"""실습 05. 실제 준비 모델을 valid에 평가합니다. test는 전달하지 않습니다."""
from pathlib import Path
import json,yaml,torch
import pandas as pd
from ultralytics import YOLO
BASE=Path(__file__).resolve().parent
if __name__=="__main__":
    torch.set_num_threads(1)
    out=BASE/"outputs";out.mkdir(exist_ok=True)
    config={"train":str(BASE/"data/images/train"),"val":str(BASE/"data/images/val"),"names":["square","circle","triangle"]}
    path=out/"dataset_active.yaml";path.write_text(yaml.safe_dump(config),encoding="utf-8")
    model=YOLO(str(BASE/"data/demo.pt"))
    # >>> A05
    # 요구: model.val에 data=path, split='val'을 전달하세요.
    pass  # TODO A05: 위 요구사항의 핵심 코드를 작성하세요.
    # <<< A05
    summary={"map50":float(metrics.box.map50),"map50_95":float(metrics.box.map),"split":"val"}
    (out/"validation_metrics.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    rows=[]
    for i,cls in enumerate(metrics.box.ap_class_index):
        pr,rc,ap50,ap=metrics.box.class_result(i)
        rows.append([int(cls),model.names[int(cls)],float(pr),float(rc),float(ap50),float(ap)])
    pd.DataFrame(rows,columns=["class_id","name","precision","recall","ap50","ap50_95"]).to_csv(out/"class_metrics.csv",index=False)
    print(summary)
