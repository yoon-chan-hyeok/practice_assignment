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

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
image = cv2.imread("data/scene.png")
# >>> TODO A01
# Matplotlib 표시 전에 BGR을 RGB로 변환하세요. 원본 image는 그대로 유지합니다.
rgb = image.copy()
# <<< TODO A01
# 각각 별도의 Figure입니다. 색공간 순서의 오류를 직접 비교합니다.
plt.figure(figsize=(5, 4)); plt.imshow(image); plt.title("Wrong: BGR interpreted as RGB"); plt.axis("off")
plt.tight_layout(); plt.savefig("outputs/p01_wrong.png", dpi=120); plt.close()
plt.figure(figsize=(5, 4)); plt.imshow(rgb); plt.title("Correct: RGB display"); plt.axis("off")
plt.tight_layout(); plt.savefig("outputs/p01_correct.png", dpi=120); plt.close()
means = image.mean(axis=(0, 1))
with open("outputs/p01_channels.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["channel", "mean"]); w.writerows(zip(["B", "G", "R"], means))
print("BGR 채널평균:", np.round(means, 3).tolist())
print("변환후 빨강:", rgb[30, 30].tolist())
