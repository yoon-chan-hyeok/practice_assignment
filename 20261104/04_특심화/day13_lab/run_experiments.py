from pathlib import Path
from time import perf_counter
from statistics import median
from dataclasses import asdict
import argparse,csv,json,os
import cv2
import numpy as np
from contracts import normalize_bgr
from geometry import Letterbox
from quality import pareto_indices,mask_metrics
from augmentation import augment
from video_pipeline import run_video

def save_csv(path,rows):
    with Path(path).open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def run_geometry(out):
    image=cv2.imread("data/scene.png")
    checked,info=normalize_bgr(image[:,::2],None)
    normalized,_=normalize_bgr(image,{(30,30):(0,0,255)})
    transform=Letterbox((225,223));resized,meta=transform(normalized)
    boxes=np.array([[0.,0.,320.,240.],[15.,15.,66.,56.]])
    mapped=transform.map_boxes(boxes,meta);restored=transform.map_boxes(mapped,meta,True)
    cv2.imwrite(str(out/"letterbox.png"),resized)
    report={"memory":info,"resize":asdict(meta),"boxes_original":boxes.tolist(),"boxes_mapped":mapped.tolist(),"roundtrip_max_error":float(np.max(np.abs(boxes-restored)))}
    (out/"geometry.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    print("좌표 왕복 일치:",np.allclose(boxes,restored,atol=1e-9))

def run_quality(out):
    noisy=cv2.imread("data/noisy_gray.png",0);clean=cv2.imread("data/clean_gray.png",0)
    rows=[]
    for border_name,border in [("reflect101",cv2.BORDER_REFLECT_101),("replicate",cv2.BORDER_REPLICATE)]:
        for k in [3,5]:
            for low,high in [(50,100),(80,160)]:
                def calculate():
                    blur=cv2.GaussianBlur(noisy,(k,k),0,borderType=border)
                    return blur,cv2.Canny(blur,low,high)
                calculate();samples=[]
                for _ in range(7):
                    start=perf_counter();filtered,edges=calculate();samples.append((perf_counter()-start)*1000)
                reference_edge=cv2.Canny(clean,low,high)>0;detected=edges>0
                tp=int(np.count_nonzero(reference_edge&detected));den=int(reference_edge.sum()+detected.sum())
                mse=float(np.mean((filtered.astype(np.float32)-clean.astype(np.float32))**2))
                name=f"{border_name}_{k}_{low}_{high}";cv2.imwrite(str(out/(name+".png")),filtered)
                rows.append({"name":name,"border":border_name,"kernel":k,"low":low,"high":high,"mse":mse,"edge_f1":2*tp/den if den else 1.0,"median_ms":median(samples)})
    selected=set(pareto_indices(rows))
    for i,row in enumerate(rows):row["pareto_mse_time"]=i in selected
    save_csv(out/"filter_benchmark.csv",rows)
    binary=cv2.imread("data/objects.png",0);reference=cv2.imread("data/mask_truth.png",0)
    rows=[]
    for k in [3,5]:
        for iterations in [1,2]:
            kernel=np.ones((k,k),np.uint8)
            result=cv2.morphologyEx(binary,cv2.MORPH_OPEN,kernel,iterations=iterations)
            metrics=mask_metrics(result,reference);metrics["kernel"]=k;metrics["iterations"]=iterations
            rows.append(metrics)
    save_csv(out/"morphology_quality.csv",rows)
    print("필터 후보:",8,"/ 형태학 후보:",len(rows))

def run_augmentation(out):
    image=cv2.imread("data/scene.png");rows=[]
    for i in range(500):
        _,meta=augment(image,42,f"distribution_{i}")
        rows.append(meta)
    save_csv(out/"augmentation_distribution.csv",rows)
    report={"n":len(rows),"flip_count":sum(r["flip"] for r in rows),"flip_rate":sum(r["flip"] for r in rows)/len(rows),"beta_min":min(r["beta"] for r in rows),"beta_max":max(r["beta"] for r in rows),"angles":sorted(set(r["angle"] for r in rows))}
    (out/"distribution.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    print("고정 ID 분포:",report)

def run_video_task(out):
    for policy,delay in [("block",0.0),("drop_latest",0.003)]:
        report=run_video("data/sample.avi",out/(policy+".avi"),policy,queue_size=2,processing_delay_s=delay)
        mapping=report.pop("frame_map");save_csv(out/(policy+"_frame_map.csv"),mapping)
        (out/(policy+".json")).write_text(json.dumps(report,indent=2),encoding="utf8")
        print(policy,"프레임 회계:",report["decoded"]==report["written"]+report["dropped"],"/ bounded:",max(report["queue_in_sampled_peak"],report["queue_out_sampled_peak"])<=2)
    print("drop_latest는 지연3ms 모의입니다. 출력 FPS 유지로 재생시간은 짧아질 수 있습니다.")

if __name__=="__main__":
    os.chdir(Path(__file__).resolve().parent);cv2.setNumThreads(1)
    p=argparse.ArgumentParser();p.add_argument("--task",choices=["geometry","quality","augment","video"],required=True);args=p.parse_args()
    out=Path("outputs")/args.task;out.mkdir(parents=True,exist_ok=True)
    {"geometry":run_geometry,"quality":run_quality,"augment":run_augmentation,"video":run_video_task}[args.task](out)
