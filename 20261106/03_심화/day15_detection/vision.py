"""모델 호출 담당. 결과를 표 형태로 바꾸며 test를 입력하지 않습니다."""
from pathlib import Path
import cv2
import pandas as pd
from ultralytics import YOLO

def detect_images(weights,folder,output,conf=.25):
    model=YOLO(str(weights));out=Path(output);out.mkdir(parents=True,exist_ok=True)
    rows=[];counts=[]
    # >>> C07
    # 요구: folder를 stream=True로 추론합니다. 결과 객체를 전부 메모리에 모으지 않습니다.
    pass  # TODO C07: 위 요구사항의 핵심 코드를 작성하세요.
    # <<< C07
    for r in results:
        image=Path(r.path).name;counts.append(dict(image=image,detections=len(r.boxes)))
        cv2.imwrite(str(out/image),r.plot())
        for box,cls,score in zip(r.boxes.xyxy.cpu().tolist(),r.boxes.cls.cpu().tolist(),r.boxes.conf.cpu().tolist()):rows.append([image,int(cls),score,*box])
    return pd.DataFrame(rows,columns=["image","class_id","confidence","x1","y1","x2","y2"]),pd.DataFrame(counts)

def track_video(weights,video,output,tracker_name='bytetrack.yaml'):
    model=YOLO(str(weights));out=Path(output);out.mkdir(parents=True,exist_ok=True)
    cap=cv2.VideoCapture(str(video))
    fps=cap.get(cv2.CAP_PROP_FPS);size=(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)));cap.release()
    writer=cv2.VideoWriter(str(out/'tracked.avi'),cv2.VideoWriter_fourcc(*'MJPG'),fps,size)
    rows=[];frames=[]
    # >>> C08
    # 요구: 새 영상용 모델에 tracker_name을 명시해 추적합니다. persist=False로 시작합니다.
    pass  # TODO C08: 위 요구사항의 핵심 코드를 작성하세요.
    # <<< C08
    for frame,r in enumerate(results):
        writer.write(r.plot());frames.append([frame,len(r.boxes)])
        if r.boxes.id is not None:
            for box,cls,tid in zip(r.boxes.xyxy.cpu().tolist(),r.boxes.cls.cpu().tolist(),r.boxes.id.cpu().tolist()):rows.append([frame,int(tid),int(cls),*box])
    writer.release()
    return pd.DataFrame(rows,columns=['frame','track_id','class_id','x1','y1','x2','y2']),pd.DataFrame(frames,columns=['frame','detections'])
