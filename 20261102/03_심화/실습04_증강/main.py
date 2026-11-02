from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent/'day11_image_classification'
sys.path.insert(0,str(PROJECT))
import torch
from torch import nn
import pandas as pd
from models import SmallCNN, build_model, set_training_mode
from data import load_data

torch.manual_seed(42)
torch.set_num_threads(1)
out=ROOT/'outputs';out.mkdir(exist_ok=True)

from PIL import Image,ImageDraw
from torchvision import transforms

image=Image.open(sorted((PROJECT/'data/train/horizontal').glob('*.png'))[0]).convert('RGB')
# BEGIN D04
# TODO D04: 라벨을 보존하는 증강 후보 3개를 구성한다.
candidates={'flip':transforms.RandomHorizontalFlip(1.0)}
# END D04
canvas=Image.new('RGB',(512,150),'white');draw=ImageDraw.Draw(canvas)
for i,(name,result) in enumerate([('original',image)]+[(name,op(image)) for name,op in candidates.items()]):
    canvas.paste(result.resize((128,128)),(128*i,22));draw.text((128*i+3,3),name,fill='black')
canvas.save(out/'augmentation_candidates.png')
print('가로/세로 라벨 보존 후보:',', '.join(candidates))
print('90도 회전은 가로/세로 라벨을 바꾸므로 제외한다.')
