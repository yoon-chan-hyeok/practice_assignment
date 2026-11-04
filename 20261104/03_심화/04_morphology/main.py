from pathlib import Path
import os
import cv2
import numpy as np

# 제공 코드: 어느 작업 폴더에서 실행해도 현재 파일 옆의 입력을 읽습니다.
# OpenCV에는 영문 상대 경로를 전달합니다. 원본 파일은 덮어쓰지 않습니다.
os.chdir(Path(__file__).resolve().parent)

import csv
import json
from time import perf_counter
Path("outputs").mkdir(exist_ok=True)

gray=cv2.imread("../data/objects.png",0)
_, binary=cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
rows=[]
for shape_name,shape in [("rect",cv2.MORPH_RECT),("ellipse",cv2.MORPH_ELLIPSE)]:
    for size in [3,5]:
        for iterations in [1,2]:
            kernel=cv2.getStructuringElement(shape,(size,size))
            # >>> TODO H04
            # 현재 kernel과 iterations를 사용하여 binary에 Opening을 적용하세요.
            result=binary.copy()
            # <<< TODO H04
            count, labels, stats, centroids=cv2.connectedComponentsWithStats(result,connectivity=8)
            name=f"{shape_name}_{size}_{iterations}"
            cv2.imwrite(f"outputs/{name}.png",result)
            rows.append([name,int(np.count_nonzero(result)),count-1])
with open("outputs/morphology.csv","w",encoding="utf-8-sig",newline="") as f:
    w=csv.writer(f);w.writerow(["setting","foreground_pixels","components_without_background"]);w.writerows(rows)
print(rows)
