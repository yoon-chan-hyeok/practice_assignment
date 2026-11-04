from pathlib import Path
import json,os

if __name__=="__main__":
    os.chdir(Path(__file__).resolve().parent)
    a=json.loads(Path("outputs/processed/cache.json").read_text(encoding="utf8"))
    b=json.loads(Path("outputs/parallel/cache.json").read_text(encoding="utf8"))
    matched=set(a)==set(b) and all(a[k]["status"]==b[k]["status"]=="ok" and a[k]["output_sha256"]==b[k]["output_sha256"] and a[k]["settings"]==b[k]["settings"] for k in a)
    print("worker1/2 설정·PNG 동일:",matched)
    if not matched:raise SystemExit(1)
