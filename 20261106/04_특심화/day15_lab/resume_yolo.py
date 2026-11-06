"""선택: 실제 Ultralytics 중단·재개 연속성. 완전 bitwise 재현을 가정하지 않습니다.
실제 run의 epoch·optimizer 보존을 검사합니다. 제작 환경 미설치로 NOT_RUN_DEPENDENCY.
weights_only=False는 이 실행이 직접 만든 로컬 checkpoint에만 사용합니다.
"""
from pathlib import Path
import argparse,json,hashlib,shutil

class PlannedStop(RuntimeError):pass

def main():
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['interrupt','resume','full']);args=parser.parse_args()
    import torch,yaml
    from ultralytics import YOLO
    base=Path(__file__).resolve().parent;out=base/'outputs/resume';out.mkdir(parents=True,exist_ok=True)
    torch.set_num_threads(1)
    cfg={'train':str(base/'data/images/train'),'val':str(base/'data/images/val'),'names':['square','circle','triangle']}
    data=out/'dataset_active.yaml';data.write_text(yaml.safe_dump(cfg),encoding='utf-8')
    if args.mode in ['interrupt','full']:
        model=YOLO('yolo26n.yaml')
        if args.mode=='interrupt':
            def stop(trainer):
                if trainer.epoch==1:
                    path=out/'interrupted.pt';shutil.copyfile(trainer.last,path)
                    ckpt=torch.load(path,map_location='cpu',weights_only=False)
                    assert ckpt['epoch']==1 and ckpt.get('optimizer') is not None
                    record=dict(epoch=ckpt['epoch'],optimizer_present=True,checkpoint_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),data_sha=hashlib.sha256((base/'data/manifest.csv').read_bytes()).hexdigest())
                    (out/'interruption.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
                    raise PlannedStop('2 epochs 이후 의도적으로 중단했습니다. resume 모드를 별도 실행하세요.')
            model.add_callback('on_model_save',stop)
        try:
            model.train(data=str(data),epochs=4,imgsz=160,batch=4,workers=0,device='cpu',amp=False,pretrained=False,optimizer='SGD',lr0=.01,seed=42,plots=False,project=str(out),name=args.mode,exist_ok=True)
        except PlannedStop as exc:print(exc)
    else:
        p=out/'interrupted.pt';record=json.loads((out/'interruption.json').read_text())
        if hashlib.sha256(p.read_bytes()).hexdigest()!=record['checkpoint_sha256']:raise ValueError('checkpoint 변경')
        if hashlib.sha256((base/'data/manifest.csv').read_bytes()).hexdigest()!=record['data_sha']:raise ValueError('분할 데이터 변경')
        ckpt=torch.load(p,map_location='cpu',weights_only=False)
        if ckpt.get('optimizer') is None:raise ValueError('추론용으로 strip된 모델은 학습 재개 증거가 아닙니다.')
        model=YOLO(str(p));model.train(resume=True,data=str(data),device='cpu',workers=0)
        print('이전 epoch:',record['epoch'],'재개 종료 epoch:',model.trainer.epoch)
        print('모델·Optimizer·배치 순서의 완전 일치는 별도 비교 필요. seed만으로 보장하지 않습니다.')

if __name__=='__main__':main()
