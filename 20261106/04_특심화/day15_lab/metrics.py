"""교육용 다중 이미지 매칭·101점 보간 AP. COCO API 완전 대체가 아닙니다."""
import numpy as np
from geometry import iou_matrix


def match_predictions(predictions,ground_truth,iou_threshold=0.5):
    if not 0<=iou_threshold<=1: raise ValueError('IoU threshold 범위')
    # >>> X04
    # 요구: dict 목록. prediction={image_id,class_id,confidence,x1,y1,x2,y2};
    # GT={image_id,class_id,x1,y1,x2,y2}. GT에는 confidence가 없다.
    # confidence 내림차순(동점=원래 순서), 같은 이미지·클래스의 아직 미사용 GT 중
    # 최대 IoU >= threshold 하나만 연결한다. 같은 정답을 두 번 TP로 만들지 않는다.
    # 반환: records(원래 prediction_index, gt_index 또는 None, tp/fp, best_iou),
    # counts={tp,fp,fn}. 다른 이미지의 정답과는 절대 연결하지 않는다.
    # 빈 prediction 또는 GT도 정상 처리. 입력 dict를 고치지 않는다.
    raise NotImplementedError("TODO X04를 구현하세요.")
    # <<< X04


def ap101(tp_flags,total_gt):
    # >>> X05
    # 요구: score순 0/1 TP 목록, 실제 GT 수>=0. total_gt=0이면 None(N/A).
    # GT>0인데 예측이 없으면 0. recall 0..1의 101점 각각에서
    # recall>=r인 지점의 최대 precision(없으면0)을 취하고 평균한다.
    # 1개 GT의 첫 예측만 TP인 중복 사례 AP는1이 될 수 있지만 FP 수는 남는다.
    # COCO의 crowd/area/maxDets/ignore 정책은 구현하지 않는다.
    raise NotImplementedError("TODO X05를 구현하세요.")
    # <<< X05


def evaluate(predictions,ground_truth,classes=(0,1,2),thresholds=None):
    thresholds=np.round(np.arange(.5,.96,.05),2) if thresholds is None else np.asarray(thresholds)
    rows=[]
    for c in classes:
        pp=[p for p in predictions if p['class_id']==c];gg=[g for g in ground_truth if g['class_id']==c]
        for threshold in thresholds:
            records,counts=match_predictions(pp,gg,float(threshold))
            rows.append(dict(class_id=int(c),iou_threshold=float(threshold),ap=ap101([r['tp'] for r in records],len(gg)),ground_truth=len(gg),**counts))
    return rows
