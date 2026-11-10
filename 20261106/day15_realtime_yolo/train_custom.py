"""선택 과제: YOLO TXT 라벨 데이터로 사전학습 모델을 추가 학습합니다. 필수 과제 아님."""
from __future__ import annotations
import argparse
import time

import torch
import yaml
from check_dataset import audit_dataset
from runtime import BASE, DEFAULT_MODEL, choose_device, environment, load_detector, new_run_dir, synchronize, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default="datasets/custom/data.yaml")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--imgsz", type=int, default=320)
    parser.add_argument("--batch", type=int, default=4)
    parser.add_argument("--device", default="auto")
    args = parser.parse_args()
    if args.epochs < 1 or args.batch < 1 or args.imgsz < 32 or args.imgsz % 32:
        raise ValueError("epochs/batch는 양수, imgsz는 32 이상인 32의 배수로 지정하세요.")
    torch.set_num_threads(4)
    # Test 폴더는 검사/학습/모델 선택에 사용하지 않습니다.
    config, audit = audit_dataset(args.data, splits=("train", "val"))
    config.pop("test", None)
    for warning in audit["warnings"]:
        print("[주의]", warning)
    output = new_run_dir("train")
    active_yaml = output / "dataset_active.yaml"
    active_yaml.write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False), encoding="utf-8")
    write_json(output / "dataset_audit.json", audit)

    # .yaml 구조 초기화가 아니라 .pt 가중치에서 시작하는 새로운 추가 학습입니다.
    # 기존 모델의 전체 클래스가 자동으로 추가/유지되는 것은 아닙니다.
    model, starting_weights = load_detector(args.model)
    device = choose_device(args.device)
    synchronize(device)
    tick = time.perf_counter()
    model.train(
        data=str(active_yaml), epochs=args.epochs, imgsz=args.imgsz, batch=args.batch,
        workers=0, device=device, amp=False, pretrained=True,
        optimizer="SGD", lr0=0.01, seed=42,
        plots=False, project=str(output.parent), name=output.name, exist_ok=True,
    )
    synchronize(device)
    elapsed = time.perf_counter() - tick
    saved_dir = model.trainer.save_dir
    best, last = saved_dir / "weights/best.pt", saved_dir / "weights/last.pt"
    if not best.is_file():
        raise RuntimeError(f"best.pt가 없습니다. 학습 로그를 확인하세요: {saved_dir}")
    write_json(output / "training_summary.json", {
        "status": "completed", "train_call_seconds": elapsed,
        "timing_scope": "model.train 호출: 데이터 준비/학습/검증/체크포인트 저장 포함. 모델 최초 로딩은 제외.",
        "requested_epochs": args.epochs, "device": device, "imgsz": args.imgsz, "batch": args.batch,
        "starting_weights": str(starting_weights), "best_pt": str(best), "last_pt": str(last),
        "names": config["names"], "environment": environment(),
    })
    # 이후 --model custom을 쓰면 가장 최근 성공한 추가 학습 모델을 불러옵니다.
    write_json(BASE / "outputs/latest_custom.json", {
        "best_pt": best.relative_to(BASE).as_posix(),
        "dataset_yaml": active_yaml.relative_to(BASE).as_posix(),
        "source_dataset_yaml": str(args.data),
    })
    print(f"\n[완료] {elapsed:.2f}초 / best: {best} / last: {last}")
    print("평가: python evaluate_custom.py")
    print("웹캠 적용: python main.py --model custom")
    print("짧은 추가 학습은 성능 향상을 보장하지 않습니다. 독립적인 valid 결과를 확인하세요.")


if __name__ == "__main__":  # Windows 멀티프로세싱 재실행 방지
    try:
        main()
    except Exception as exc:
        print(f"[학습 실패] {exc}")
        raise SystemExit(1)
