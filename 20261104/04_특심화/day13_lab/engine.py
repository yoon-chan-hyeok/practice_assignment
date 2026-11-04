"""제공 골격: manifest 기반 병렬 처리·실패 기록·재개. TODO는 작은 핵심 함수에 집중합니다."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
import csv,hashlib,json,re
import cv2
import numpy as np
from augmentation import augment
from geometry import Letterbox
from cache import cache_key,can_reuse,atomic_bytes

def worker_init():
    cv2.setNumThreads(1)

def process_job(job):
    # 한 항목의 실패가 나머지 정상 항목의 결과를 숨기지 않도록 구조화해서 반환합니다.
    entry,raw,config=job
    try:
        image=cv2.imdecode(np.frombuffer(raw,np.uint8),cv2.IMREAD_COLOR)
        if image is None:raise ValueError("decode 실패")
        out,settings=augment(image,config["seed"],entry["sample_id"],split=entry["split"],allow_flip=entry["allow_flip"]=="1",allow_rotate=True)
        resized,info=Letterbox(tuple(config["size"]))(out)
        gray=cv2.cvtColor(resized,cv2.COLOR_BGR2GRAY)
        blur=cv2.GaussianBlur(gray,(config["blur"],config["blur"]),0)
        result=cv2.Canny(blur,*config["canny"])
        ok,encoded=cv2.imencode(".png",result)
        if not ok:raise OSError("PNG encode 실패")
        content=encoded.tobytes()
        return {"sample_id":entry["sample_id"],"split":entry["split"],"status":"ok","shape":list(result.shape),"dtype":str(result.dtype),"settings":settings,"output_sha256":hashlib.sha256(content).hexdigest()},content
    except (ValueError,TypeError,OSError,cv2.error) as exc:
        return {"sample_id":entry["sample_id"],"split":entry["split"],"status":"failed","error":str(exc)},None

def run_images(data_root,out_root,config,workers=1,resume=False):
    data_root,out_root=Path(data_root).resolve(),Path(out_root).resolve()
    if out_root==data_root or out_root.is_relative_to(data_root):raise ValueError("결과 폴더는 data 밖이어야 합니다")
    if not isinstance(workers,int) or workers<1:raise ValueError("workers는 양의 정수")
    if set(config)!={"size","seed","blur","canny"}:raise ValueError("알 수 없거나 누락된 config")
    Letterbox(tuple(config["size"]))
    if config["blur"]<=0 or config["blur"]%2!=1 or len(config["canny"])!=2 or not 0<=config["canny"][0]<=config["canny"][1]:raise ValueError("필터 설정 오류")
    out_root.mkdir(parents=True,exist_ok=True)
    cache_path=out_root/"cache.json"
    previous=json.loads(cache_path.read_text(encoding="utf8")) if resume and cache_path.exists() else {}
    with (data_root/"manifest.csv").open(encoding="utf-8-sig",newline="") as f:entries=list(csv.DictReader(f))
    ids=[r["sample_id"] for r in entries]
    if len(ids)!=len(set(ids)) or any(not re.fullmatch(r"[A-Za-z0-9_-]+",id) for id in ids):raise ValueError("ID는 고유한 영문·숫자·_·-만 허용")
    result={};pending=[];keys={}
    for entry in entries:
        id=entry["sample_id"];source=(data_root/entry["path"]).resolve()
        if not source.is_relative_to(data_root):raise ValueError("data 밖의 경로 금지")
        try:
            raw=source.read_bytes();key=cache_key(raw,config,id,entry["split"]);keys[id]=key
            destination=out_root/(id+".png")
            if resume and can_reuse(previous.get(id),key,destination):
                result[id]={**previous[id],"reused":True}
            else:pending.append((entry,raw,config))
        except OSError as exc:
            result[id]={"sample_id":id,"split":entry["split"],"status":"failed","error":str(exc),"reused":False}
    if workers==1:
        worker_init();processed=list(map(process_job,pending))
    elif pending:
        with ProcessPoolExecutor(max_workers=workers,mp_context=mp.get_context("spawn"),initializer=worker_init) as pool:
            processed=list(pool.map(process_job,pending))
    else:processed=[]
    for entry,content in processed:
        id=entry["sample_id"];entry["key"]=keys[id];entry["reused"]=False
        if content is not None:atomic_bytes(out_root/(id+".png"),content)
        result[id]=entry
    ordered={id:result[id] for id in ids}
    atomic_bytes(cache_path,json.dumps(ordered,ensure_ascii=False,sort_keys=True,indent=2).encode())
    with (out_root/"events.jsonl").open("a",encoding="utf8") as f:
        for record in ordered.values():f.write(json.dumps(record,ensure_ascii=False,sort_keys=True)+"\n")
    summary={"total":len(ids),"ok":sum(r["status"]=="ok" for r in ordered.values()),"failed":sum(r["status"]!="ok" for r in ordered.values()),"reused":sum(r.get("reused",False) for r in ordered.values()),"workers":workers,"records":ordered}
    return summary
