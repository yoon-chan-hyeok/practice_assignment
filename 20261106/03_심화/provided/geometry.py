"""좌표 계약. 함수 문법보다 단위·범위·경계 정의가 중요합니다."""
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Box:
    x1: float
    y1: float
    x2: float
    y2: float

    def __post_init__(self):
        # float64 계산 전에 NaN/inf와 역전·영면적 박스를 차단한다.
        values=np.asarray([self.x1,self.y1,self.x2,self.y2],dtype=float)
        if not np.isfinite(values).all() or self.x2<=self.x1 or self.y2<=self.y1:
            raise ValueError('유한한 x1<x2, y1<y2 박스가 필요합니다.')

    def to_yolo(self, width: int, height: int) -> np.ndarray:
        # 요구: W/H는 양의 정수. 박스가 이미지 안에 완전히 있어야 한다.
        # 반환: float64 [cx/W, cy/H, w/W, h/H]. 연속 경계여서 +1을 쓰지 않는다.
        # 원본 객체를 바꾸지 않으며 결과 배열은 새로 만든다. 잘못된 입력은 ValueError.
        # 허용오차: from_yolo와 왕복했을 때 1e-6 px 이내.
        # 해설: 중심과 크기는 다른 뜻이다. 각각의 축 길이로 따로 나눈다.
        _image_size(width,height)
        if not (0<=self.x1<self.x2<=width and 0<=self.y1<self.y2<=height):
            raise ValueError('박스가 이미지 경계 밖입니다.')
        return np.array([(self.x1+self.x2)/(2*width),(self.y1+self.y2)/(2*height),(self.x2-self.x1)/width,(self.y2-self.y1)/height],dtype=np.float64)

    @classmethod
    def from_yolo(cls, values, width: int, height: int):
        _image_size(width,height)
        v=np.asarray(values,dtype=float)
        if v.shape!=(4,) or not np.isfinite(v).all() or (v<0).any() or (v>1).any() or (v[2:]<=0).any():
            raise ValueError('정규화 중심·크기 4개가 필요합니다.')
        cx,cy,w,h=v*np.array([width,height,width,height])
        box=cls(cx-w/2,cy-h/2,cx+w/2,cy+h/2)
        if box.x1 < -1e-6 or box.y1 < -1e-6 or box.x2 > width+1e-6 or box.y2 > height+1e-6:
            raise ValueError('중심이 정상이어도 박스 가장자리가 경계 밖일 수 있습니다.')
        return box

    def clip(self, width: int, height: int):
        _image_size(width,height)
        return Box(max(0,self.x1),max(0,self.y1),min(width,self.x2),min(height,self.y2))


def _image_size(width,height):
    if isinstance(width,bool) or isinstance(height,bool) or not isinstance(width,(int,np.integer)) or not isinstance(height,(int,np.integer)) or width<=0 or height<=0:
        raise ValueError('양의 정수 width·height가 필요합니다.')


def as_boxes(value):
    a=np.asarray(value,dtype=np.float64)
    if a.size==0 and a.shape in [(0,),(0,4)]: return a.reshape(0,4)
    if a.ndim!=2 or a.shape[1]!=4 or not np.isfinite(a).all() or np.any(a[:,2:]<=a[:,:2]):
        raise ValueError('유한한 양의 면적을 가진 Nx4 xyxy가 필요합니다.')
    return a


def iou_matrix(a,b):
    a,b=as_boxes(a),as_boxes(b)
    # 요구: (N,4),(M,4) -> (N,M) float64. N/M=0이면 해당 빈 행렬을 반환.
    # 접촉만 한 박스는 IoU=0. 이미지 밖 좌표도 양의 면적이면 계산 가능하다.
    # 면적 = (x2-x1)*(y2-y1), +1 금지. 입력 배열 in-place 변경 금지.
    # 정상 입력의 결과는 [0,1], 자체 박스 IoU는 1. 수치 오차 허용 1e-12.
    # 해설: broadcast로 N×M 쌍의 겹치는 폭·높이를 계산한다.
    lo=np.maximum(a[:,None,:2],b[None,:,:2]); hi=np.minimum(a[:,None,2:],b[None,:,2:])
    intersection=np.prod(np.maximum(hi-lo,0),axis=-1)
    area_a=np.prod(a[:,2:]-a[:,:2],axis=-1);area_b=np.prod(b[:,2:]-b[:,:2],axis=-1)
    return intersection/(area_a[:,None]+area_b[None,:]-intersection)


def class_nms(boxes,scores,classes,threshold=0.5):
    b=as_boxes(boxes);s=np.asarray(scores,dtype=float);c=np.asarray(classes)
    if s.shape!=(len(b),) or c.shape!=(len(b),) or not np.isfinite(s).all() or np.any((s<0)|(s>1)) or not 0<=threshold<=1:
        raise ValueError('score/class/threshold 계약 불일치')
    if not np.issubdtype(c.dtype,np.integer) or np.any(c<0): raise ValueError('class는 음이 아닌 정수')
    # 요구: 원래 행 index를 score 내림차순으로 반환. 동점은 입력 순서 유지.
    # 같은 클래스 AND IoU > threshold인 나중 후보만 제거한다(=이면 보존).
    # 서로 다른 클래스는 겹쳐도 보존. threshold 범위는 위에서 검사됨.
    # 빈 입력 -> []이며 원본 boxes/scores/classes를 수정하지 않는다.
    # 해설: 이 함수는 고전 NMS 원리용이다. YOLO26 기본 end-to-end 추론과 별개다.
    order=np.argsort(-s,kind='stable').tolist();keep=[]
    while order:
        i=order.pop(0);keep.append(i)
        if order:
            overlaps=iou_matrix(b[[i]],b[order])[0]
            order=[j for j,ov in zip(order,overlaps) if not(c[j]==c[i] and ov>threshold)]
    return keep
