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

from filters import apply_filter
from statistics import median

gray = cv2.imread("../data/noisy_gray.png",0)
rows=[]
for name in ["gaussian","sharpen","bilateral"]:
    apply_filter(gray,name)  # 워밍업 제외
    samples=[]
    for _ in range(7):
        start=perf_counter(); result=apply_filter(gray,name); samples.append((perf_counter()-start)*1000)
    edge=cv2.Canny(result,80,160)
    cv2.imwrite(f"outputs/{name}.png",result);cv2.imwrite(f"outputs/{name}_edge.png",edge)
    rows.append([name,median(samples),int(np.count_nonzero(edge))])
with open("outputs/filter_comparison.csv","w",encoding="utf-8-sig",newline="") as f:
    w=csv.writer(f);w.writerow(["filter","median_ms","edge_pixels"]);w.writerows(rows)
print("필터/Edge 픽셀:",[(r[0],r[2]) for r in rows])
print("median_ms는 현재 CPU·OpenCV 환경의 7회 측정값입니다.")
