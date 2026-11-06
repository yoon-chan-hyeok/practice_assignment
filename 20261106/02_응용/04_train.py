"""실습 04. API 학습과 같은 설정의 CLI 명령을 기록합니다."""
from pathlib import Path
import yaml,torch
from ultralytics import YOLO
BASE=Path(__file__).resolve().parent
if __name__=="__main__":
    torch.set_num_threads(1)
    out=BASE/"outputs";out.mkdir(exist_ok=True)
    config={"train":str(BASE/"data/images/train"),"val":str(BASE/"data/images/val"),"names":["square","circle","triangle"]}
    path=out/"dataset_active.yaml";path.write_text(yaml.safe_dump(config),encoding="utf-8")
    model=YOLO("yolo26n.yaml")
    # >>> A04
    # 요구: 2 epoch smoke 학습을 실행하세요. seed·imgsz·batch·optimizer 조건을 고정합니다.
    pass  # TODO A04: 위 요구사항의 핵심 코드를 작성하세요.
    # <<< A04
    command=f'yolo detect train model=yolo26n.yaml data="{path}" epochs=2 imgsz=160 batch=4 workers=0 device=cpu amp=False pretrained=False optimizer=SGD lr0=0.01 seed=42 plots=False project="{out}" name=cli_smoke exist_ok=True'
    (out/"same_settings_cli.txt").write_text(command,encoding="utf-8")
    print("best/last:",out/"smoke/weights", "CLI 비교는 선택 실행입니다.")
