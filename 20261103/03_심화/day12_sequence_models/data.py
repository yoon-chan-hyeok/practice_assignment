"""제공 모듈: 시간 구간/독립 ID 분할을 읽는다. test는 반환하지 않는다."""
from pathlib import Path
import json
import pandas as pd
import torch
from torch.nn.utils.rnn import pad_sequence

def forecast_data(folder, variable=False):
    frame = pd.read_csv(Path(folder)/'series.csv')
    result = {}
    for split in ['train', 'valid']:
        part = frame[frame['split']==split]
        values = torch.tensor(part['value'].values, dtype=torch.float32)
        windows = values.unfold(0,13,1)
        lengths = torch.tensor([6+i%7 for i in range(len(windows))]) if variable else torch.full((len(windows),),12)
        seqs = [w[12-int(length):12].unsqueeze(-1) for w,length in zip(windows,lengths)]
        result[split] = {'x':pad_sequence(seqs,batch_first=True), 'lengths':lengths,
                         'y':windows[:,12:13].clone(), 'ids':part['time'].tolist()[12:]}
    return result

def reconstruction_data(folder, noisy=False):
    frame = pd.read_csv(Path(folder)/'series.csv'); result={}
    for i,split in enumerate(['train','valid']):
        part=frame[frame['split']==split]
        clean=torch.tensor(part['value'].values,dtype=torch.float32).unfold(0,8,1).contiguous()
        generator=torch.Generator().manual_seed(120400+i)
        noise=torch.randn(clean.shape,generator=generator)*0.12 if noisy else torch.zeros_like(clean)
        result[split]={'x':clean+noise,'y':clean,'lengths':None,'ids':part['time'].tolist()[7:]}
    return result

def classification_data(folder):
    items=json.loads((Path(folder)/'sequences.json').read_text(encoding='utf-8')); result={}
    for split in ['train','valid']:
        records=[r for r in items if r['split']==split]
        result[split]={'x':pad_sequence([torch.tensor(r['values']) for r in records],batch_first=True),
            'lengths':torch.tensor([r['length'] for r in records]),
            'y':torch.tensor([r['label'] for r in records]),'ids':[r['id'] for r in records]}
    return result
