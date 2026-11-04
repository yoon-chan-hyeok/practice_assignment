from pathlib import Path
import os
import cv2
import numpy as np

# 제공 코드: 어느 작업 폴더에서 실행해도 현재 파일 옆의 입력을 읽습니다.
# OpenCV에는 영문 상대 경로를 전달합니다. 원본 파일은 덮어쓰지 않습니다.
os.chdir(Path(__file__).resolve().parent)

# 색상 이미지: 한 픽셀의 값 순서는 B, G, R입니다.
# >>> TODO B01
# scene.png를 cv2.imread로 읽어 image에 저장하세요. flags를 생략하면 BGR 컬러로 읽습니다.
image = None
# <<< TODO B01
print("shape:", image.shape)
print("dtype:", image.dtype)
print("min/max:", int(image.min()), int(image.max()))
print("빨강 패치의 BGR:", image[30, 30].tolist())
saved = cv2.imwrite("p01_copy.png", image)
print("PNG 저장:", saved)
