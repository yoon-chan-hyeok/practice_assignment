import argparse, json
from pathlib import Path
from tasks import probe_device

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--device", choices=["cpu","auto","cuda"], default="cpu")
    args=parser.parse_args()
    result=probe_device(args.device)
    out=Path(__file__).resolve().parent/"outputs";out.mkdir(exist_ok=True)
    (out/"environment.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__ == "__main__": main()
