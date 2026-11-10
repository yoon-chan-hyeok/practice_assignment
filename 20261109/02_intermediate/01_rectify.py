from pathlib import Path
import json
import re
import numpy as np
import pandas as pd
import cv2
base = Path(__file__).resolve().parent
data = base / 'data'
out = base / 'outputs'
out.mkdir(exist_ok=True)
lesson = json.loads((data / 'lesson.json').read_text(encoding='utf-8'))

image = cv2.imread(str(data / 'perspective.png'))
corners = np.float32(lesson['perspective']['corners'])  # TL, TR, BR, BL 제공
size = (1000, 700)  # width, height
matrix = cv2.getPerspectiveTransform(corners, np.float32([[0,0],[999,0],[999,699],[0,699]]))
# TODO A01
rectified = cv2.resize(image, size)
# TODO 끝 A01
gray = cv2.cvtColor(rectified, cv2.COLOR_BGR2GRAY)
adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 11)
cv2.imwrite(str(out / 'p01_rectified.png'), rectified)
cv2.imwrite(str(out / 'p01_adaptive.png'), adaptive)
print('before:', image.shape, 'after:', rectified.shape)
print('알려진 모서리로 보정했습니다. 모서리 자동 검출이 아닙니다.')
