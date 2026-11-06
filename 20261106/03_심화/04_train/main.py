"""실습 04. imgsz 한 조건만 바꾼 1 epoch 연결 점검입니다."""
from pathlib import Path
from time import perf_counter
import yaml,torch
import pandas as pd
from ultralytics import YOLO
BASE=Path(__file__).resolve().parent
if __name__=="__main__":
    torch.set_num_threads(1)
    out=BASE/"outputs";out.mkdir(exist_ok=True);data=BASE.parent/"data"
    p=out/"dataset_active.yaml"
    p.write_text(yaml.safe_dump({"train":str(data/"images/train"),"val":str(data/"images/val"),"names":["square","circle","triangle"]}),encoding="utf-8")
    rows=[]
    for size in [160,192]:
        torch.manual_seed(42);model=YOLO("yolo26n.yaml");start=perf_counter()
        # >>> C04
        # 요구: 현재 size만 imgsz로 바꿔 학습하세요. 다른 조건은 고정합니다.
        # 이 짧은 실험은 속도·파일 생성 확인이며 최적 모델 순위를 결론 내리지 않습니다.
        pass  # TODO C04: 위 요구사항의 핵심 코드를 작성하세요.
        # <<< C04
        rows.append(dict(imgsz=size,parameters=sum(t.numel() for t in model.model.parameters()),seconds=perf_counter()-start,map50=float(model.metrics.box.map50),map50_95=float(model.metrics.box.map)))
    pd.DataFrame(rows).to_csv(out/"size_comparison.csv",index=False)
    print(pd.DataFrame(rows).to_string(index=False))
