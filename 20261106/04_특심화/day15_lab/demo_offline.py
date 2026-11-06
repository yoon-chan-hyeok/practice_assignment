"""특심화의 독립 검증 데모. fixture를 실제 YOLO 결과로 표시하지 않습니다."""
from pathlib import Path
import json
import pandas as pd
from metrics import evaluate,match_predictions
from audit import audit_dataset
from tracking import IoUTracker,count_id_switches
from artifacts import run_artifacts
BASE=Path(__file__).resolve().parent

def fixture_processor(path):
    return dict(backend='teaching_fixture',filename=path.name,rows=len(pd.read_csv(path)))

if __name__=='__main__':
    out=BASE/'outputs';out.mkdir(exist_ok=True)
    p=pd.read_csv(BASE/'data/boxes_fixture.csv').to_dict('records');g=pd.read_csv(BASE/'data/boxes_gt.csv').to_dict('records')
    _,counts=match_predictions(p,g);ap=pd.DataFrame(evaluate(p,g));ap.to_csv(out/'educational_ap.csv',index=False)
    audit,issues=audit_dataset(BASE/'data');pd.DataFrame(audit).to_csv(out/'audit.csv',index=False)
    gt=pd.read_csv(BASE/'data/track_ground_truth.csv');tracker=IoUTracker();pred=[]
    for frame,batch in gt.groupby('frame',sort=True):
        # 입력은 정확한 기하 정답을 검출로 가장한 원리 fixture. 실제 탐지 성능이 아니다.
        boxes=batch[['x1','y1','x2','y2']].to_numpy(float)+1
        ids=tracker.update('simulation',int(frame),boxes,batch.class_id.to_numpy())
        for row,tid,box in zip(batch.to_dict('records'),ids,boxes):pred.append(dict(frame=int(frame),track_id=tid,class_id=row['class_id'],**dict(zip(['x1','y1','x2','y2'],box))))
    pd.DataFrame(pred).to_csv(out/'fixture_tracks.csv',index=False)
    switches=count_id_switches(gt.to_dict('records'),pred)
    manifest=run_artifacts([BASE/'data/boxes_fixture.csv'],out/'artifacts',{'backend':'teaching_fixture'},fixture_processor)
    result=dict(backend='teaching_fixture',matching=counts,label_issues=len(issues),tracking=switches,artifact_status=manifest)
    (out/'offline_summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
