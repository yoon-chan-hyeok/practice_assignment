from pathlib import Path
import argparse,json,os
from engine import run_images

if __name__=="__main__":
    os.chdir(Path(__file__).resolve().parent)
    parser=argparse.ArgumentParser(description="Day13 Config 기반 전처리. 원본은 수정하지 않습니다.")
    parser.add_argument("--workers",type=int,default=1)
    parser.add_argument("--resume",action="store_true")
    parser.add_argument("--output",default="outputs/processed")
    args=parser.parse_args()
    config=json.loads(Path("config.json").read_text(encoding="utf8"))
    result=run_images("data",args.output,config,args.workers,args.resume)
    summary={k:v for k,v in result.items() if k!="records"}
    print(json.dumps(summary,ensure_ascii=False,sort_keys=True))
    Path(args.output,"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf8")
    if result["failed"]:raise SystemExit(1)
