"""IoU 연결 원리 전용 추적기. ByteTrack/BoT-SORT/YOLO 구현이라고 부르지 않는다."""
import numpy as np
from geometry import iou_matrix,as_boxes

class IoUTracker:
    def __init__(self,threshold=.3,max_gap=2):
        if not 0<=threshold<=1 or max_gap<0:raise ValueError('추적 설정')
        self.threshold=threshold;self.max_gap=max_gap;self.streams={}

    def reset(self,stream):
        self.streams.pop(str(stream),None)

    def update(self,stream,frame,boxes,classes):
        # >>> X07
        # 요구: stream별 독립 ID 공간(각각1부터). 같은 stream의 frame은 엄격히 증가.
        # boxes Nx4, classes N. 이전 track은 frame-last_seen<=max_gap일 때만 후보.
        # 같은 class·IoU>=threshold 쌍을 IoU 내림차순, 동점 trackID/검출index순으로
        # greedy 1:1 연결한다. 남은 검출에 신규 ID 부여. 반환은 검출 순서의 ID 목록.
        # 빈 frame도 last_frame을 진행하고 만료 track 제거. 다른 stream 상태 불변.
        # 실제 ByteTrack 대신 쓰는 production tracker가 아니라 수치 검증용 원리 모델.
        raise NotImplementedError("TODO X07를 구현하세요.")
        # <<< X07


def count_id_switches(gt_rows,pred_rows,threshold=.5):
    """교육용: 연속 두 프레임에서 매칭된 같은 GT의 예측 ID가 바뀌는 횟수. MOT 공식 지표 아님."""
    previous={};switches=0;matches=0
    frames=sorted({r['frame'] for r in gt_rows})
    keys=['x1','y1','x2','y2']
    for frame in frames:
        gt=[r for r in gt_rows if r['frame']==frame];pred=[r for r in pred_rows if r['frame']==frame]
        pairs=[]
        for gi,g in enumerate(gt):
            for pi,p in enumerate(pred):
                if g['class_id']==p['class_id']:
                    ov=float(iou_matrix([[g[k] for k in keys]],[[p[k] for k in keys]])[0,0])
                    if ov>=threshold:pairs.append((-ov,gi,pi))
        seen_g=set();seen_p=set()
        for _,gi,pi in sorted(pairs):
            if gi in seen_g or pi in seen_p:continue
            seen_g.add(gi);seen_p.add(pi);g=gt[gi];p=pred[pi];matches+=1
            old=previous.get(g['gt_id'])
            if old is not None and old[0]==frame-1 and old[1]!=p['track_id']:switches+=1
            previous[g['gt_id']]=(frame,p['track_id'])
    return dict(continuous_match_id_switches=switches,matched_objects=matches,definition='consecutive_matched_frames_only')
