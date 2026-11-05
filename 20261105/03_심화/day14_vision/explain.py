"""Grad-CAM과 오류 이미지 저장. 임의 예시 열지도를 성능 증거로 만들지 않습니다."""
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
import cv2
import torch


def cam_for(model,x,target):
    """소형 Sequential 전용. Parameter의 기존 .grad를 건드리지 않습니다."""
    flags=[(m,m.training) for m in model.modules()];model.eval()
    try:
        with torch.enable_grad():
            image=x.detach().clone().requires_grad_(True)
            activation=model[:7](image);logits=model[7:](activation)
            grad=torch.autograd.grad(logits[0,target],activation)[0]
            cam=(grad.mean((2,3),keepdim=True)*activation).sum(1).relu()
            cam=torch.nn.functional.interpolate(cam.unsqueeze(1),x.shape[-2:],mode='bilinear',align_corners=False)[0,0]
            return (cam/cam.max().clamp_min(1e-8)).detach().cpu().numpy()
    finally:
        for m,flag in flags:m.training=flag


def save_explanations(data,out,model,prediction):
    """정답·오답 각각 최대 1장 CAM, 실제 오답 최대 8장. 없는 오류를 조작하지 않습니다."""
    from engine import datasets
    _,valid=datasets(data);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    for stale in out.glob('error_*.png'):stale.unlink()
    for stale in out.glob('cam_*.png'):stale.unlink()
    wrong=prediction.index[prediction.actual!=prediction.predicted].tolist()
    correct=prediction.index[prediction.actual==prediction.predicted].tolist()
    for index in wrong[:8]:
        row=prediction.loc[index];image=Image.open(Path(data)/row.path).convert('RGB').resize((192,192))
        tile=Image.new('RGB',(192,240),'white');tile.paste(image,(0,0));d=ImageDraw.Draw(tile)
        d.text((4,195),f'true: {valid.classes[int(row.actual)]}',fill='black')
        d.text((4,210),f'pred: {valid.classes[int(row.predicted)]}',fill='black')
        d.text((4,225),f'p={row.confidence:.3f}',fill='black');tile.save(out/f'error_{index:03d}.png')
    records=[]
    for kind,indices in [('correct',correct),('wrong',wrong)]:
        if not indices:continue
        index=indices[0];x,_=valid[index];target=int(prediction.loc[index,'predicted']);cam=cam_for(model,x[None],target)
        rgb=np.uint8(x.permute(1,2,0).numpy()*255)
        overlay=cv2.addWeighted(cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR),.6,cv2.applyColorMap(np.uint8(cam*255),cv2.COLORMAP_JET),.4,0)
        cv2.imwrite(str(out/f'cam_{kind}.png'),cv2.resize(overlay,(256,256)))
        records.append({'kind':kind,'path':prediction.loc[index,'path'],'target_class':target})
    return records
