"""실습 07~08. Tracker 두 종류를 독립 인스턴스로 비교합니다."""
from pathlib import Path
from time import perf_counter
import cv2,torch
import pandas as pd
from ultralytics import YOLO
BASE=Path(__file__).resolve().parent
out=BASE/"outputs";out.mkdir(exist_ok=True);torch.set_num_threads(1)
summaries=[]
for name in ["bytetrack.yaml","botsort.yaml"]:
    model=YOLO(str(BASE/"data/demo.pt"))  # 비교마다 상태가 새로 시작됩니다.
    rows=[];frame_counts=[];start=perf_counter()
    writer=cv2.VideoWriter(str(out/(Path(name).stem+".avi")),cv2.VideoWriter_fourcc(*"MJPG"),10,(160,128))
    # >>> A07
    # 요구: demo.avi를 현재 name의 tracker로 track 하세요. 반환은 stream generator입니다.
    pass  # TODO A07: 위 요구사항의 핵심 코드를 작성하세요.
    # <<< A07
    for frame,r in enumerate(results):
        writer.write(r.plot());frame_counts.append([frame,len(r.boxes)])
        if r.boxes.id is not None:
            for box,cls,score,tid in zip(r.boxes.xyxy.cpu().tolist(),r.boxes.cls.cpu().tolist(),r.boxes.conf.cpu().tolist(),r.boxes.id.cpu().tolist()):
                rows.append([frame,int(tid),int(cls),score,*box])
    writer.release();seconds=perf_counter()-start
    # >>> A08
    # 요구: tracker별 CSV에 frame·track_id·class_id·confidence·xyxy를 저장하세요.
    pass  # TODO A08: 위 요구사항의 핵심 코드를 작성하세요.
    # <<< A08
    pd.DataFrame(frame_counts,columns=["frame","detections"]).to_csv(out/(Path(name).stem+"_frames.csv"),index=False)
    summaries.append(dict(tracker=name,frames=len(frame_counts),track_rows=len(rows),seconds=seconds,throughput=len(frame_counts)/seconds,scope="decode+infer+track+plot+encode; first-run cost included",id_switch="별도 GT 매칭 필요"))
r=pd.DataFrame(summaries);r.to_csv(out/"tracker_comparison.csv",index=False);print(r.to_string(index=False))
