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

def letterbox(image, size=(224, 224)):
    """비율을 유지해 채운 뒤 남는 가장자리에 검정을 추가합니다. size=(W,H)."""
    height, width = image.shape[:2]
    ratio = min(size[0]/width, size[1]/height)
    new_w, new_h = round(width*ratio), round(height*ratio)
    left = (size[0]-new_w)//2; top = (size[1]-new_h)//2
    # >>> TODO H02
    # new_w·new_h로 Resize한 뒤 top/bottom/left/right 여백을 추가해 size와 같은 크기를 만드세요. result에 저장합니다.
    result = cv2.resize(image, size)
    # <<< TODO H02
    return result, {"resized_wh":[new_w,new_h],"left":left,"top":top,"ratio":ratio}

image = cv2.imread("../data/scene.png")
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, (35,80,60), (85,255,255))
masked = cv2.bitwise_and(image, image, mask=mask)
result, settings = letterbox(image)
cv2.imwrite("outputs/green_mask.png", mask);cv2.imwrite("outputs/green_only.png", masked)
cv2.imwrite("outputs/letterbox.png", result)
Path("outputs/resize.json").write_text(json.dumps(settings,indent=2),encoding="utf-8")
print("Letterbox:",result.shape,settings)
print("녹색 Mask 픽셀:",int(np.count_nonzero(mask)))
