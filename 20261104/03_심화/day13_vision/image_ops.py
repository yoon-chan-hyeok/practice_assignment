import cv2
import numpy as np

def prepare_image(image,size=(160,120)):
    """색공간·Resize·필터·형태학 처리의 중간 결과를 딕셔너리로 반환합니다."""
    # >>> TODO H07
    # Gray와 size=(너비,높이)로 축소한 small을 만드세요. 원본 image를 직접 수정하지 않습니다.
    gray=image[:,:,0]
    small=cv2.resize(gray,size)
    # <<< TODO H07
    blur=cv2.GaussianBlur(small,(3,3),0)
    _,binary=cv2.threshold(blur,127,255,cv2.THRESH_BINARY)
    kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    opened=cv2.morphologyEx(binary,cv2.MORPH_OPEN,kernel)
    edge=cv2.Canny(blur,80,160)
    return {"gray":gray,"small":small,"blur":blur,"binary":binary,"opened":opened,"edge":edge}

def augment_image(image):
    """종합 실습에서는 설정을 고정해 재실행 비교를 쉽게 합니다."""
    flipped=cv2.flip(image,1)
    return np.clip(flipped.astype(np.float32)+15,0,255).astype(np.uint8)
