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

image = cv2.imread("../data/scene.png")
# >>> TODO H01
# IMREAD_GRAYSCALE로 scene.png를, IMREAD_UNCHANGED로 rgba.png를 읽으세요. 변수 이름은 gray, rgba입니다.
gray = image.copy()
rgba = cv2.imread("../data/rgba.png")
# <<< TODO H01
cv2.imwrite("outputs/lossless.png", image)
cv2.imwrite("outputs/lossy.jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 80])
rows = []
for filename in ["lossless.png", "lossy.jpg"]:
    p = Path("outputs") / filename
    readback = cv2.imread(str(p))
    mae = float(np.abs(image.astype(np.float32) - readback.astype(np.float32)).mean())
    rows.append([filename, p.stat().st_size, round(mae, 5), np.array_equal(image, readback)])
with open("outputs/format_comparison.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["file", "bytes", "pixel_mae", "pixel_equal"]); w.writerows(rows)
print("Gray/UNCHANGED shape:", gray.shape, rgba.shape)
print("Alpha range:", int(rgba[:,:,3].min()), int(rgba[:,:,3].max()))
print(rows)
