"""교육용 다중 이미지 매칭·101점 보간 AP. COCO API 완전 대체가 아닙니다."""
import numpy as np
from geometry import iou_matrix


def match_predictions(predictions,ground_truth,iou_threshold=0.5):
    if not 0<=iou_threshold<=1: raise ValueError('IoU threshold 범위')
    # 요구: dict 목록. prediction={image_id,class_id,confidence,x1,y1,x2,y2};
    # GT={image_id,class_id,x1,y1,x2,y2}. GT에는 confidence가 없다.
    # confidence 내림차순(동점=원래 순서), 같은 이미지·클래스의 아직 미사용 GT 중
    # 최대 IoU >= threshold 하나만 연결한다. 같은 정답을 두 번 TP로 만들지 않는다.
    # 반환: records(원래 prediction_index, gt_index 또는 None, tp/fp, best_iou),
    # counts={tp,fp,fn}. 다른 이미지의 정답과는 절대 연결하지 않는다.
    # 빈 prediction 또는 GT도 정상 처리. 입력 dict를 고치지 않는다.
    # 해설: Greedy matching의 순서와 중복 검출을 구분하는 핵심이다.
    keys=['x1','y1','x2','y2'];used=set();records=[]
    for pi in sorted(range(len(predictions)),key=lambda i:(-predictions[i]['confidence'],i)):
        p=predictions[pi]
        eligible=[j for j,g in enumerate(ground_truth) if j not in used and g['image_id']==p['image_id'] and g['class_id']==p['class_id']]
        gi=None;best=0.0
        if eligible:
            ovs=iou_matrix([[p[k] for k in keys]],[[ground_truth[j][k] for k in keys] for j in eligible])[0]
            best=float(ovs.max());candidate=eligible[int(ovs.argmax())]
            if best>=iou_threshold: gi=candidate;used.add(gi)
        records.append(dict(prediction_index=pi,gt_index=gi,tp=int(gi is not None),fp=int(gi is None),best_iou=best))
    tp=len(used)
    return records,dict(tp=tp,fp=len(predictions)-tp,fn=len(ground_truth)-tp)


def ap101(tp_flags,total_gt):
    # 요구: score순 0/1 TP 목록, 실제 GT 수>=0. total_gt=0이면 None(N/A).
    # GT>0인데 예측이 없으면 0. recall 0..1의 101점 각각에서
    # recall>=r인 지점의 최대 precision(없으면0)을 취하고 평균한다.
    # 1개 GT의 첫 예측만 TP인 중복 사례 AP는1이 될 수 있지만 FP 수는 남는다.
    # COCO의 crowd/area/maxDets/ignore 정책은 구현하지 않는다.
    # 해설: AP는 지정 confidence 하나의 precision과 다르다.
    if total_gt<0: raise ValueError('total_gt 음수')
    flags=np.asarray(tp_flags)
    if flags.ndim!=1 or np.any((flags!=0)&(flags!=1)) or flags.sum()>total_gt: raise ValueError('TP flags 계약')
    if total_gt==0:return None
    if len(flags)==0:return 0.0
    tp=np.cumsum(flags);recall=tp/total_gt;precision=tp/np.arange(1,len(tp)+1)
    return float(np.mean([precision[recall>=r].max() if np.any(recall>=r) else 0.0 for r in np.linspace(0,1,101)]))


def evaluate(predictions,ground_truth,classes=(0,1,2),thresholds=None):
    thresholds=np.round(np.arange(.5,.96,.05),2) if thresholds is None else np.asarray(thresholds)
    rows=[]
    for c in classes:
        pp=[p for p in predictions if p['class_id']==c];gg=[g for g in ground_truth if g['class_id']==c]
        for threshold in thresholds:
            records,counts=match_predictions(pp,gg,float(threshold))
            rows.append(dict(class_id=int(c),iou_threshold=float(threshold),ap=ap101([r['tp'] for r in records],len(gg)),ground_truth=len(gg),**counts))
    return rows
