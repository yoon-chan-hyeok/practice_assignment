"""완성 선행 엔진 + 이번 교시 데이터/기록 과제. python run.py --device cpu"""
import argparse,csv,json
from pathlib import Path
import torch
from tasks import load_development,build_loaders,write_predictions
from model import SimpleANN
from engine import train_one_epoch,evaluate

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--device',choices=['cpu','auto','cuda'],default='cpu')
    args=parser.parse_args();torch.set_num_threads(1);torch.manual_seed(42)
    device=torch.device('cuda:0' if args.device=='cuda' or (args.device=='auto' and torch.cuda.is_available()) else 'cpu')
    if device.type=='cuda' and not torch.cuda.is_available(): raise RuntimeError('명시한 CUDA를 사용할 수 없습니다.')
    base=Path(__file__).resolve().parent;out=base/'outputs';out.mkdir(exist_ok=True)
    tensors,ids=load_development(base/'data/points.csv');train,valid,g=build_loaders(tensors)
    model=SimpleANN().to(device);opt=torch.optim.SGD(model.parameters(),lr=0.1)
    history=[]
    for epoch in range(1,81):
        trained=train_one_epoch(model,train,opt,device);checked=evaluate(model,valid,device)
        history.append([epoch,trained['loss'],checked['loss'],checked['accuracy']])
    write_predictions(out/'validation_predictions.csv',ids['valid'],tensors['valid'][1],checked['probabilities'])
    with (out/'training_history.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['epoch','train_loss_online','valid_loss','valid_accuracy']);w.writerows(history)
    report={'train_samples':len(ids['train']),'valid_samples':len(ids['valid']),'test_ids_only':len(ids['test']),'test_used':False,'epochs':80,'valid_loss':checked['loss'],'valid_accuracy':checked['accuracy'],'device':str(device)}
    (out/'final_metrics.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    (out/'split_manifest.json').write_text(json.dumps(ids,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
