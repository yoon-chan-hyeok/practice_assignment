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

import hashlib
with open("outputs/result_summary.csv",encoding="utf-8-sig",newline="") as f:
    rows=list(csv.DictReader(f))
checks=[]
for row in rows:
    image=cv2.imread(row["output"],cv2.IMREAD_UNCHANGED)
    # >>> TODO H10
    # 읽은 image의 존재·(높이,너비)·dtype·채널을 CSV와 비교해 bool ok를 만드세요. 보고서의 의미 판단을 자동 채점하는 코드는 아닙니다.
    ok = False
    # <<< TODO H10
    checks.append(ok)
original_hashes=json.loads(Path("outputs/source_hashes.json").read_text(encoding="utf-8"))
source_unchanged=all(hashlib.sha256((Path("data")/name).read_bytes()).hexdigest()==digest for name,digest in original_hashes.items())
video=cv2.VideoCapture("outputs/processed.avi");count=0;shapes=[]
while video.isOpened():
    ok,frame=video.read()
    if not ok:break
    count+=1;shapes.append(frame.shape)
fps=video.get(cv2.CAP_PROP_FPS);video.release()
report={"image_rows":len(rows),"images_ok":len(rows)==21 and all(checks),"source_unchanged":source_unchanged,"video_ok":count==48 and fps==12 and all(s==(120,160,3) for s in shapes)}
Path("outputs/validation.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(report)
