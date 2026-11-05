from pathlib import Path
import sys,json
import numpy as np
import pandas as pd
import torch
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE.parent/"day14_vision"))
DATA=BASE.parent/"data"
OUT=BASE/"outputs"
OUT.mkdir(exist_ok=True)
torch.set_num_threads(1)
from engine import experiment,datasets,metrics
from models import build_model,configure
from explain import cam_for
import cv2
model,_,_,prediction=experiment(DATA,epochs=8)
_,valid=datasets(DATA);x,_=valid[0];x=x[None]
# 중심 24×24만 유지하는 조작. 대상 일부도 지울 수 있으므로 원인 증명으로 쓰지 않습니다.
changed=x.clone();changed[:,:,:4,:]=0;changed[:,:,-4:,:]=0;changed[:,:,:,:4]=0;changed[:,:,:,-4:]=0
with torch.no_grad():
    original_prob=model(x).softmax(1)
    changed_prob=model(changed).softmax(1)
target=int(original_prob.argmax(1).item())
# TODO D06: 두 입력에 같은 target을 고정하여 비교하세요.
# BEGIN D06
cams=[cam_for(model,x,target),cam_for(model,x,target)]  # 두 번째는 changed를 사용하세요.
# END D06
for name,tensor,cam in zip(["original","occluded"],[x,changed],cams):
    rgb=np.uint8(tensor[0].permute(1,2,0).numpy()*255)
    overlay=cv2.addWeighted(cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR),.6,cv2.applyColorMap(np.uint8(cam*255),cv2.COLORMAP_JET),.4,0)
    cv2.imwrite(str(OUT/f"{name}.png"),cv2.resize(overlay,(256,256)))
print("고정 target:",target)
print("원본 확률:",round(original_prob[0,target].item(),4),"가림 확률:",round(changed_prob[0,target].item(),4))
