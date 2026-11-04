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

from video_ops import process_frame
cap=cv2.VideoCapture("../data/sample.avi");fps=cap.get(cv2.CAP_PROP_FPS)
writer=cv2.VideoWriter("outputs/edge.avi",cv2.VideoWriter_fourcc(*"MJPG"),fps,(160,120))
count=0;processing=[];start_all=perf_counter()
while cap.isOpened() and writer.isOpened():
    ok,frame=cap.read()
    if not ok: break
    start=perf_counter();result=process_frame(frame);processing.append(perf_counter()-start)
    writer.write(result);count+=1
cap.release();writer.release();wall=perf_counter()-start_all
check=cv2.VideoCapture("outputs/edge.avi")
report={"frames_written":count,"reopened_frames":int(check.get(7)),"fps":check.get(5),"width":int(check.get(3)),"height":int(check.get(4)),"wall_s":wall,"mean_process_ms":float(np.mean(processing)*1000)}
check.release()
Path("outputs/video_report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print("Frame/FPS/크기:",report["reopened_frames"],report["fps"],(report["width"],report["height"]))
print("wall은 read·처리·write 포함, mean_process는 Frame 처리만 포함합니다.")
