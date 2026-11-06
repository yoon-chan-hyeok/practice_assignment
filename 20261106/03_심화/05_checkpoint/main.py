"""실습 05. 이전 실습의 best와 last를 동일한 valid에 평가합니다."""
from pathlib import Path
import torch
import pandas as pd
from ultralytics import YOLO
BASE=Path(__file__).resolve().parent
if __name__=="__main__":
    torch.set_num_threads(1)
    out=BASE/"outputs";out.mkdir(exist_ok=True)
    train=BASE.parent/"04_train/outputs"
    rows=[]
    for name in ["best","last"]:
        model=YOLO(str(train/f"size160/weights/{name}.pt"))
        # >>> C05
        # 요구: 같은 dataset_active.yaml과 imgsz로 split='val' 평가를 호출하세요.
        # 1 epoch 학습에서는 best와 last의 예측이 같아도 정상입니다.
        pass  # TODO C05: 위 요구사항의 핵심 코드를 작성하세요.
        # <<< C05
        rows.append(dict(checkpoint=name,map50=float(m.box.map50),map50_95=float(m.box.map)))
    pd.DataFrame(rows).to_csv(out/"checkpoint_comparison.csv",index=False);print(pd.DataFrame(rows).to_string(index=False))
