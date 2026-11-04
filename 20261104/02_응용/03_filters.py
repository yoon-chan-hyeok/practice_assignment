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

gray = cv2.imread("data/noisy_gray.png", cv2.IMREAD_GRAYSCALE)
# >>> TODO A03
# 같은 gray에 Gaussian (5,5), sigmaX=0과 Median ksize=5를 각각 적용하세요.
gaussian = gray.copy()
median = gray.copy()
# <<< TODO A03
rows = []
for name, result in [("original", gray), ("gaussian", gaussian), ("median", median)]:
    edge = cv2.Canny(result, 80, 160)
    cv2.imwrite(f"outputs/p03_{name}.png", result)
    cv2.imwrite(f"outputs/p03_{name}_edge.png", edge)
    rows.append([name, int(np.count_nonzero(edge))])
with open("outputs/p03_edges.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["filter", "edge_pixels"]); w.writerows(rows)
print(rows)
print("Edge가 많다고 무조건 좋지 않습니다. 잡음 경계일 수도 있습니다.")
