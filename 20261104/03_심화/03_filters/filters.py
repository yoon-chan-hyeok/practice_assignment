import cv2
import numpy as np

def apply_filter(gray, name):
    """한 장의 Gray에 선택 필터를 적용합니다. 파일 입출력은 하지 않습니다."""
    if name == "gaussian":
        return cv2.GaussianBlur(gray,(5,5),0)
    if name == "sharpen":
        kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]],dtype=np.float32)
        return cv2.filter2D(gray,-1,kernel)
    # >>> TODO H03
    # 마지막 후보 bilateral을 d=7, sigmaColor=50, sigmaSpace=50으로 처리해 반환하세요. name은 정상 후보만 전달됩니다.
    return gray.copy()
    # <<< TODO H03
