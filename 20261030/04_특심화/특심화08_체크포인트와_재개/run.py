"""독립 실행. full/first/resume를 각각 새 Python 프로세스에서 실행합니다."""
from pathlib import Path
import sys,subprocess,json,argparse
import torch
from tasks import compare_states
BASE=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--part',choices=['full','first','resume']);args=parser.parse_args()
    if args.part:
        from engine import execute
        execute(args.part);return
    for part in ['full','first','resume']:
        subprocess.run([sys.executable,str(Path(__file__).resolve()),'--part',part],check=True,cwd=BASE)
    out=BASE/'outputs'
    a=torch.load(out/'full.pt',map_location='cpu',weights_only=True)
    b=torch.load(out/'resumed.pt',map_location='cpu',weights_only=True)
    mismatches=compare_states(a,b)
    checks={key:not compare_states(a[key],b[key],key) for key in a}
    report={'continued_epochs':20,'resumed_from':10,'checks':checks,'all_equal':not mismatches,
            'mismatch_paths':mismatches,'scope':'Same CPU/version; epoch boundary; num_workers=0; no AMP/distributed',
            'test_used':False}
    (out/'resume_report.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    print(json.dumps(report,indent=2))
    if mismatches: raise AssertionError('연속/재개 상태 불일치')
if __name__=='__main__':main()
