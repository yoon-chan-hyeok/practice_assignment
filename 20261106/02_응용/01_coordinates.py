"""실습 01. 픽셀 xyxy와 YOLO 정규화 중심·크기를 왕복합니다."""
from pathlib import Path
import numpy as np
import pandas as pd
BASE=Path(__file__).resolve().parent
out=BASE/"outputs";out.mkdir(exist_ok=True)
table=pd.read_csv(BASE/"data/boxes_gt.csv")
b=table[["x1","y1","x2","y2"]].to_numpy(float);width,height=160,128
# >>> A01
# 요구: 중심 x/y와 폭/높이를 계산하고 각 축 크기로 정규화하세요.
pass  # TODO A01: 위 요구사항의 핵심 코드를 작성하세요.
# <<< A01
pixel=yolo*np.array([width,height,width,height])
restored=np.column_stack((pixel[:,0]-pixel[:,2]/2,pixel[:,1]-pixel[:,3]/2,pixel[:,0]+pixel[:,2]/2,pixel[:,1]+pixel[:,3]/2))
print("최대 왕복 오차(px):", float(np.max(np.abs(b-restored))))
pd.DataFrame(yolo,columns=["cx","cy","w","h"]).to_csv(out/"yolo_coordinates.csv",index=False)
