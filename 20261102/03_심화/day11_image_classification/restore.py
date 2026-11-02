"""저장된 모델은 다시 다운로드하지 않는다. 신뢰하는 자체 checkpoint만 읽는다."""
from pathlib import Path
import argparse
import json
import torch
import pandas as pd
from data import load_data
from models import build_model
from train import evaluate

ROOT=Path(__file__).resolve().parent
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('--name',default='small')
    args=parser.parse_args()
    torch.set_num_threads(1)
    saved=torch.load(ROOT/'outputs'/f'best_{args.name}.pt',map_location='cpu',weights_only=True)
    model=build_model(saved['kind'],width=saved['width'],pretrained=False)
    # BEGIN D10
    # TODO D10: 저장된 state_dict를 복원한 구조에 적재한다.
    pass
    # END D10
    train,_,valid,_,_,loader=load_data(saved['kind'])
    loss,accuracy,logits,labels=evaluate(model,loader,torch.device('cpu'))
    previous=pd.read_csv(ROOT/'outputs'/f'predictions_{args.name}.csv')
    paths=[Path(p).relative_to(ROOT/'data').as_posix() for p,_ in valid.samples]
    same_ids=paths==previous.file.tolist()
    same_pred=logits.argmax(1).tolist()==previous.predicted.tolist()
    same_probability=torch.allclose(logits.softmax(1)[:,1],torch.tensor(previous.probability_vertical.values,dtype=torch.float32),atol=1e-5,rtol=1e-5)
    report=dict(same_ids=same_ids,same_classes=train.class_to_idx==saved['class_to_idx'],
                same_predictions=same_pred,same_probability=same_probability,valid_loss=loss,valid_accuracy=accuracy)
    (ROOT/'outputs'/'restore_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(report)
