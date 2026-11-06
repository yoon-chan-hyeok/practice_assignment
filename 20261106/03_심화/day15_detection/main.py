"""실습 07. 데이터 감사와 실제 YOLO 추론·추적을 연결합니다."""
from pathlib import Path
import json,hashlib,shutil
import torch
from vision import detect_images,track_video
BASE=Path(__file__).resolve().parent
if __name__=='__main__':
    torch.set_num_threads(1)
    out=BASE/'outputs';out.mkdir(exist_ok=True)
    weight=BASE/'data/demo.pt'
    predictions,counts=detect_images(weight,BASE/'data/images/val',out/'images')
    tracks,frames=track_video(weight,BASE/'data/demo.avi',out)
    predictions.to_csv(out/'predictions.csv',index=False);counts.to_csv(out/'image_counts.csv',index=False)
    tracks.to_csv(out/'tracks.csv',index=False);frames.to_csv(out/'frames.csv',index=False)
    # >>> C09
    # 요구: 실제 처리한 이미지 수·프레임 수·모델 해시를 기록하세요.
    pass  # TODO C09: 위 요구사항의 핵심 코드를 작성하세요.
    # <<< C09
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    shutil.copyfile(weight,out/'model.pt')  # 신뢰하는 자체 준비 모델을 함께 보관합니다.
    print(json.dumps(summary,ensure_ascii=False,indent=2))
