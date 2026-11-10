"""선택 과제: 정답 라벨이 있는 val에서 mAP 평가. Test는 --split test를 명시한 경우에만 사용."""
from __future__ import annotations
import argparse
import csv
import json
import math
import time

import torch
import yaml
from check_dataset import audit_dataset
from runtime import BASE, choose_device, environment, load_detector, new_run_dir, project_path, synchronize, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="custom")
    parser.add_argument("--data", default=None)
    parser.add_argument("--split", choices=("val", "test"), default="val")
    parser.add_argument("--imgsz", type=int, default=320)
    parser.add_argument("--batch", type=int, default=4)
    parser.add_argument("--device", default="auto")
    args = parser.parse_args()
    torch.set_num_threads(4)
    data_file = args.data
    if data_file is None:
        pointer = BASE / "outputs/latest_custom.json"
        if not pointer.is_file():
            raise FileNotFoundError("추가 학습 결과가 없습니다. 먼저 학습하거나 --data와 --model을 지정하세요.")
        info = json.loads(pointer.read_text(encoding="utf-8"))
        # val은 학습 때 생성한 절대경로 YAML, test는 원래 사용자가 지정한 YAML 사용
        data_file = info["dataset_yaml"] if args.split == "val" else info["source_dataset_yaml"]
    config, audit = audit_dataset(data_file, splits=(args.split,))
    model, weights = load_detector(args.model)
    trained_names = [model.names[i] for i in range(len(model.names))]
    if trained_names != config["names"]:
        raise ValueError("모델 클래스와 YAML names가 다릅니다. 이름만 바꿔 재해석하지 말고 실제 라벨 ID/학습 모델을 확인하세요.")
    if args.split == "val":
        config.pop("test", None)
    output = new_run_dir("eval")
    active = output / "dataset_active.yaml"
    active.write_text(yaml.safe_dump(config, sort_keys=False, allow_unicode=True), encoding="utf-8")
    write_json(output / "dataset_audit.json", audit)
    device = choose_device(args.device)
    synchronize(device)
    tick = time.perf_counter()
    # 웹캠 표시 임계값 0.25와 다릅니다. PR 곡선 평가를 위해 낮은 후보 임계값을 사용합니다.
    metrics = model.val(data=str(active), split=args.split, imgsz=args.imgsz, batch=args.batch,
                        workers=0, device=device, conf=0.001, plots=False,
                        project=str(output.parent), name=output.name, exist_ok=True)
    synchronize(device)
    def number(value):
        value = float(value)
        return value if math.isfinite(value) else None
    summary = {
        "split": args.split, "weights": str(weights), "names": config["names"],
        "precision_mean": number(metrics.box.mp), "recall_mean": number(metrics.box.mr),
        "map50": number(metrics.box.map50), "map50_95": number(metrics.box.map),
        "val_call_seconds": time.perf_counter()-tick,
        "imgsz": args.imgsz, "batch": args.batch, "device": device, "candidate_conf": 0.001,
        "note": "mAP는 accuracy가 아닙니다. 웹캠 실시간 품질과 동일한 평가가 아닙니다.",
        "environment": environment(),
    }
    write_json(output / "metrics.json", summary)
    with (output / "class_metrics.csv").open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["class_id", "name", "precision", "recall", "ap50", "ap50_95"])
        for i, cls in enumerate(metrics.box.ap_class_index):
            pr, rc, ap50, ap = metrics.box.class_result(i)
            writer.writerow([int(cls), model.names[int(cls)], number(pr), number(rc), number(ap50), number(ap)])
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print("결과 폴더:", output)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[평가 실패] {exc}")
        raise SystemExit(1)
