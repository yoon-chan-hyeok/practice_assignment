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

def augment(image,seed):
    rng=np.random.default_rng(seed)
    flip=bool(rng.random()<0.5); beta=int(rng.integers(-20,21))
    result=cv2.flip(image,1) if flip else image.copy()
    # >>> TODO H06
    # beta를 적용하되 uint8의 순환을 막고 값 범위를 지키세요. 원본 image는 수정하지 않습니다.
    result=result.copy()
    # <<< TODO H06
    return result,{"seed":seed,"flip":flip,"beta":beta}

with open("../data/manifest.csv",encoding="utf-8-sig",newline="") as f:
    sources=list(csv.DictReader(f))
rows=[]
for row in sorted(sources,key=lambda r:r["sample_id"]):
    if row["split"]!="train":
        continue  # valid/test는 증강 대상이 아닙니다.
    seed=42+int(row["sample_id"].split("_")[-1])
    src=Path("../data")/row["path"];image=cv2.imread(str(src))
    result,settings=augment(image,seed);dest=Path("outputs")/(row["sample_id"]+"_aug.png")
    saved=cv2.imwrite(str(dest),result)
    rows.append([row["sample_id"],row["split"],str(dest),seed,settings["flip"],settings["beta"],saved,hashlib.sha256(src.read_bytes()).hexdigest()])
with open("outputs/augmentation.csv","w",encoding="utf-8-sig",newline="") as f:
    w=csv.writer(f);w.writerow(["id","split","output","seed","flip","beta","saved","source_sha256"]);w.writerows(rows)
print("증강 이미지:",len(rows),"/ train만 처리")
print("설정:",[(r[0],r[3],r[4],r[5]) for r in rows])
