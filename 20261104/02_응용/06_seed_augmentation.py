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

def augment(image, seed):
    """로컬 난수로 밝기·좌우반전을 결정합니다. 입력 배열은 변경하지 않습니다."""
    rng = np.random.default_rng(seed)
    flip = bool(rng.random() < 0.5)
    beta = int(rng.integers(-25, 26))
    result = image.copy()
    if flip:
        result = cv2.flip(result, 1)
    # >>> TODO A06
    # float32에서 beta를 더하고 [0,255]로 clip한 뒤 uint8로 돌리세요. uint8 상태로 직접 더하지 않습니다.
    result = result.copy()
    # <<< TODO A06
    return result, {"seed": seed, "flip": flip, "beta": beta}

image = cv2.imread("data/scene.png")
first, settings = augment(image, 42)
second, _ = augment(image, 42)
cv2.imwrite("outputs/p06_comparison.png", cv2.hconcat([image, first, second]))
Path("outputs/p06_settings.json").write_text(json.dumps(settings, indent=2), encoding="utf-8")
print("같은 seed 결과 일치:", np.array_equal(first, second))
print("설정:", settings)
