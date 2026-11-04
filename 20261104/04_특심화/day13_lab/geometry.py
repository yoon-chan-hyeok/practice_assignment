from dataclasses import dataclass
import cv2
import numpy as np
from contracts import normalize_bgr

@dataclass(frozen=True)
class ResizeInfo:
    source_hw: tuple
    target_wh: tuple
    resized_wh: tuple
    pad_ltrb: tuple
    scale_xy: tuple

class Letterbox:
    """좌표는 픽셀 경계 좌표계 [0,W]×[0,H]. 픽셀 중심 보간식과 혼동하지 않습니다."""
    def __init__(self,size=(224,224),interpolation=cv2.INTER_AREA):
        if len(size)!=2 or any(not isinstance(v,int) or isinstance(v,bool) or v<=0 for v in size):
            raise ValueError("size는 양의 정수 (W,H)")
        self.size=tuple(size);self.interpolation=interpolation

    def __call__(self,image):
        image,_=normalize_bgr(image)
        # >>> TODO X02
        # 요구사항 X02 — 비율 유지 Resize와 역변환에 필요한 메타데이터.
        # 입력은 normalize_bgr를 통과한 정상 배열입니다. self.size=(target_width,target_height).
        # r=min(target_width/W,target_height/H). new width/height는 round 후 최소1, 목표 크기 이하로 제한합니다.
        # 남는 여백은 좌/상에 //2, 나머지를 우/하에 배치합니다. 검정 BGR(0,0,0)으로 채웁니다.
        # 반환은 (image_out, ResizeInfo). 정확한 target H×W×3와 uint8을 유지해야 합니다.
        # 정수 반올림 후 실제 scale_x=new_width/W, scale_y=new_height/H를 별도로 저장합니다.
        # 이상적인 r 하나만 저장하면 비정방 입력의 역변환이 어긋날 수 있습니다.
        # 원본 훼손 금지. 1픽셀 입력, 홀수 여백, 큰 확대에도 음수 여백을 만들지 않습니다.
        raise NotImplementedError("TODO X02: 요구사항을 구현하세요")
        # <<< TODO X02

    @staticmethod
    def map_points(points,info,inverse=False):
        # >>> TODO X03
        # 요구사항 X03 — 순방향·역방향 좌표 변환.
        # points는 N×2, 순서는 (x,y). 빈 N=0은 허용하고 NaN/inf·잘못된 shape는 ValueError입니다.
        # 순방향: (x*scale_x+left, y*scale_y+top). 역방향은 패딩을 빼고 실제 배율로 나눕니다.
        # 출력 float64, 입력 보존. 기본 경로는 clipping·정수 반올림을 하지 않습니다.
        # 이 계약은 xyxy 박스의 픽셀 경계 좌표입니다. cv2.resize의 픽셀 중심 보간 위치와 다릅니다.
        # map_boxes가 두 끝점에 재사용합니다. 홀수 크기 원본의 왕복 오차 <=1e-9를 만족하세요.
        # 이미지 패딩 영역의 좌표는 역변환 시 원본 바깥일 수 있습니다. 조용히 잘라내지 마세요.
        raise NotImplementedError("TODO X03: 요구사항을 구현하세요")
        # <<< TODO X03

    @staticmethod
    def map_boxes(boxes,info,inverse=False):
        boxes=np.asarray(boxes,dtype=np.float64)
        if boxes.ndim!=2 or boxes.shape[1]!=4 or not np.isfinite(boxes).all():
            raise ValueError("boxes는 유한한 N×4 xyxy")
        if np.any(boxes[:,2:]<boxes[:,:2]):raise ValueError("뒤집힌 박스")
        a=Letterbox.map_points(boxes[:,:2],info,inverse)
        b=Letterbox.map_points(boxes[:,2:],info,inverse)
        return np.concatenate([a,b],axis=1)
