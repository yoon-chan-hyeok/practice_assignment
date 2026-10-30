"""다른 실습 결과 없이 baseline을 만들고 새 프로세스에서 재개합니다. CPU 동일 환경 검증입니다."""
from pathlib import Path
import argparse,json,subprocess,sys
import torch
from data import CONFIG,load_development,make_loaders
from model import SimpleANN
from engine import train_one_epoch,evaluate
from tasks import save_checkpoint,restore_checkpoint,same_state

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--resume',action='store_true');args=parser.parse_args()
    torch.set_num_threads(1)
    base=Path(__file__).resolve().parent;out=base/'outputs';out.mkdir(exist_ok=True)
    config=dict(CONFIG,device='cpu',momentum=0.9)
    # momentum의 내부식은 다음 수업입니다. 여기서는 실제 상태를 가지는 Optimizer를 제공받습니다.
    torch.manual_seed(999 if args.resume else 42)
    g=torch.Generator().manual_seed(999 if args.resume else 43)
    tensors,ids=load_development();train,valid=make_loaders(tensors,g)
    model=SimpleANN();opt=torch.optim.SGD(model.parameters(),lr=0.1,momentum=0.9)
    start=restore_checkpoint(out/'checkpoint_mid.pt',model,opt,g,config,ids,torch.device('cpu')) if args.resume else 0
    for epoch in range(start+1,81):
        train_one_epoch(model,train,opt,torch.device('cpu'))
        result=evaluate(model,valid,torch.device('cpu'))
        if not args.resume and epoch==40:
            save_checkpoint(out/'checkpoint_mid.pt',model,opt,epoch,g,config,ids)
    target=out/('checkpoint_resumed.pt' if args.resume else 'checkpoint_final.pt')
    save_checkpoint(target,model,opt,80,g,config,ids)
    if args.resume:
        return
    subprocess.run([sys.executable,str(Path(__file__).resolve()),'--resume'],cwd=base,check=True)
    ref=torch.load(out/'checkpoint_final.pt',weights_only=True,map_location='cpu')
    got=torch.load(out/'checkpoint_resumed.pt',weights_only=True,map_location='cpu')
    checks={key:same_state(ref[key],got[key]) for key in ref}
    report={'continued_epochs':80,'resumed_from':40,'checks':checks,'all_equal':all(checks.values()),'scope':'same CPU environment; epoch boundary; num_workers=0','test_used':False}
    (out/'resume_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
    if not report['all_equal']:raise AssertionError('연속 학습과 재개 상태가 다릅니다.')
if __name__=='__main__': main()
