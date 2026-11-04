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
from image_ops import prepare_image,augment_image
from video_ops import process_video

rows=[];source_hashes={}
for filename in ["scene.png","noisy.png","objects.png"]:
    src=Path("data")/filename;source_hashes[filename]=hashlib.sha256(src.read_bytes()).hexdigest()
    image=cv2.imread(str(src));start=perf_counter();results=prepare_image(image);seconds=perf_counter()-start
    results["aug"]=augment_image(cv2.resize(image,(160,120),interpolation=cv2.INTER_AREA))
    # >>> TODO H09
    # results의 각 stage/result를 PNG로 저장하고 재읽기 비교와 크기·채널을 rows에 기록하세요. CSV 열은 코드의 예시 구조를 참고합니다.
    pass
    # <<< TODO H09
    preview=cv2.hconcat([cv2.resize(image,(160,120)),cv2.cvtColor(results["small"],cv2.COLOR_GRAY2BGR),cv2.cvtColor(results["edge"],cv2.COLOR_GRAY2BGR)])
    cv2.imwrite(f"outputs/{src.stem}_compare.png",preview)
source_hashes["sample.avi"]=hashlib.sha256(Path("data/sample.avi").read_bytes()).hexdigest()
video=process_video("data/sample.avi","outputs/processed.avi")
with open("outputs/result_summary.csv","w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
Path("outputs/source_hashes.json").write_text(json.dumps(source_hashes,indent=2),encoding="utf-8")
Path("outputs/video_report.json").write_text(json.dumps(video,indent=2),encoding="utf-8")
print("이미지 처리표:",len(rows),"행")
print("영상 Frame/FPS:",video["decoded"],video["fps"])
print("다음: python validate.py")
