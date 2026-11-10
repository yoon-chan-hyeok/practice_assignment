"""
Day15 1시간 프로젝트: 사전학습 YOLO로 노트북 카메라 실시간 객체 탐지.
기본 실행: python main.py  |  S: 증빙 이미지 저장  |  Q/ESC: 종료
학습 없이 박스·클래스·confidence를 표시하고 실행 로그를 자동 저장합니다.
웹캠에는 정답 라벨이 없으므로 accuracy/mAP를 계산하지 않습니다.
"""
from __future__ import annotations

import argparse
import csv
from collections import deque
from contextlib import ExitStack
import time

import cv2
import numpy as np
import torch
import yaml

from runtime import (
    BASE, choose_device, environment, load_detector, new_run_dir,
    open_capture, project_path, save_png, sha256, synchronize, write_json,
)


def parse_args():
    # 기본 설정은 config.yaml, 명령행 옵션이 있으면 해당 값만 덮어씁니다.
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("model", "source", "device"):
        parser.add_argument(f"--{name}")
    parser.add_argument("--conf", type=float)
    parser.add_argument("--imgsz", type=int)
    parser.add_argument("--no-display", action="store_true", help="GUI 없는 환경/자동 점검용")
    parser.add_argument("--max-frames", type=int, default=0, help="0이면 Q/ESC 또는 영상 끝까지")
    parser.add_argument("--snapshot-every", type=int, default=0, help="선택: N프레임마다 캡처. 기본 비활성")
    return parser.parse_args()


def run(args) -> dict:
    config = yaml.safe_load((BASE / "config.yaml").read_text(encoding="utf-8"))
    for key in ("model", "source", "device", "conf", "imgsz"):
        if getattr(args, key) is not None:
            config[key] = getattr(args, key)
    if not 0 <= config["conf"] <= 1 or config["imgsz"] < 32 or config["imgsz"] % 32:
        raise ValueError("conf는 0~1, imgsz는 32 이상인 32의 배수(256/320/640 등)로 지정하세요.")
    if args.max_frames < 0 or args.snapshot_every < 0:
        raise ValueError("프레임 수는 0 이상으로 지정하세요.")

    # 숫자는 카메라 번호, 그 외 문자열은 로컬 영상 파일 경로입니다.
    source_text = str(config["source"])
    source = int(source_text) if source_text.isdigit() else str(project_path(source_text))
    if isinstance(source, str) and not project_path(source).is_file():
        raise FileNotFoundError(f"영상 파일이 없습니다: {source}")
    if args.no_display and isinstance(source, int) and args.max_frames == 0:
        raise ValueError("카메라를 화면 없이 실행할 때는 --max-frames 100처럼 종료 조건을 지정하세요.")

    torch.set_num_threads(int(config["cpu_threads"]))
    device = choose_device(config["device"])
    model, weight_path = load_detector(config["model"])
    output = new_run_dir("webcam")
    shots = output / "snapshots"
    shots.mkdir()
    print(f"[실행] source={source} / device={device} / conf={config['conf']} / imgsz={config['imgsz']}")
    print("[조작] 영상 창을 클릭한 뒤 S=캡처, Q 또는 ESC=종료")
    print(f"[저장] {output}")

    capture = None
    frame_count = detection_count = detected_frames = snapshot_count = 0
    predict_times, loop_times = [], []
    recent = deque(maxlen=30)
    status, error = "completed", None
    window = "Day15 YOLO | S: snapshot | Q/ESC: quit"
    actual_size = None
    started = time.perf_counter()

    try:
        capture = open_capture(source)
        if isinstance(source, int):
            capture.set(cv2.CAP_PROP_FRAME_WIDTH, config["camera_width"])
            capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config["camera_height"])
        ok, frame = capture.read()
        if not ok or frame is None:
            raise RuntimeError("카메라는 열렸지만 첫 프레임을 읽지 못했습니다. 권한/장치 번호를 확인하세요.")
        actual_size = [int(frame.shape[1]), int(frame.shape[0])]

        # 모델 초기 준비 비용을 일반 프레임 처리 시간에서 제외합니다.
        for _ in range(2):
            model.predict(np.zeros_like(frame), conf=config["conf"], imgsz=config["imgsz"], device=device, verbose=False)
        synchronize(device)
        if not args.no_display:
            cv2.namedWindow(window, cv2.WINDOW_NORMAL)

        with ExitStack() as stack:
            def csv_writer(filename, columns):
                file = stack.enter_context((output / filename).open("w", newline="", encoding="utf-8-sig"))
                writer = csv.writer(file)
                writer.writerow(columns)
                return writer
            frames = csv_writer("frames.csv", ["frame_index", "detections", "predict_call_ms", "loop_ms"])
            detections = csv_writer("detections.csv", ["frame_index", "class_id", "class_name", "confidence", "x1", "y1", "x2", "y2"])
            snapshots = csv_writer("snapshots.csv", ["frame_index", "raw_file", "annotated_file", "detections"])
            first = True
            while True:
                loop_start = time.perf_counter()
                if not first:
                    ok, frame = capture.read()
                    if not ok or frame is None:
                        if isinstance(source, int):
                            raise RuntimeError("카메라 프레임 수신이 중단되었습니다.")
                        break  # 파일 영상 끝. 정상 종료와 디코딩 실패는 별도 확인 필요.
                first = False

                # ① 학습된 모델로 한 프레임 추론. 가중치는 업데이트하지 않습니다.
                synchronize(device)
                tick = time.perf_counter()
                result = model.predict(
                    frame, conf=config["conf"], imgsz=config["imgsz"],
                    device=device, verbose=False,
                )[0]
                synchronize(device)
                predict_ms = (time.perf_counter() - tick) * 1000

                # ② 탐지 결과를 CPU로 가져와 기록하고 화면에 박스/이름/점수를 표시합니다.
                boxes = result.boxes
                xyxy = boxes.xyxy.cpu().numpy()
                scores = boxes.conf.cpu().tolist()
                classes = boxes.cls.int().cpu().tolist()
                annotated = result.plot()
                fps = 1000 / np.mean(recent) if recent else 0.0
                cv2.putText(annotated, f"Loop FPS {fps:.1f} | conf {config['conf']:.2f} | boxes {len(classes)}",
                            (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
                cv2.putText(annotated, "S: save evidence   Q/ESC: exit", (10, 48),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                key = -1
                if not args.no_display:
                    cv2.imshow(window, annotated)
                    key = cv2.waitKey(1) & 0xFF

                # ③ S를 누른 프레임만 원본/주석 이미지를 저장합니다. 기본은 녹화하지 않습니다.
                periodic = args.snapshot_every > 0 and (frame_count + 1) % args.snapshot_every == 0
                if key in (ord("s"), ord("S")) or periodic:
                    stem = f"frame_{frame_count:06d}"
                    raw_path, annotated_path = shots / f"{stem}_raw.png", shots / f"{stem}_annotated.png"
                    save_png(raw_path, frame)
                    save_png(annotated_path, annotated)
                    snapshots.writerow([frame_count, str(raw_path.relative_to(output)), str(annotated_path.relative_to(output)), len(classes)])
                    snapshot_count += 1
                    print(f"[캡처] {annotated_path.name}")

                # CSV는 매 프레임 기록. 같은 물체의 반복 탐지를 고유 객체 수로 해석하지 않습니다.
                for cls, score, coords in zip(classes, scores, xyxy):
                    detections.writerow([frame_count, cls, result.names[cls], f"{score:.6f}", *map(float, coords)])
                loop_ms = (time.perf_counter() - loop_start) * 1000
                frames.writerow([frame_count, len(classes), round(predict_ms, 4), round(loop_ms, 4)])
                predict_times.append(predict_ms)
                loop_times.append(loop_ms)
                recent.append(loop_ms)
                frame_count += 1
                detection_count += len(classes)
                detected_frames += int(bool(classes))
                if key in (ord("q"), ord("Q"), 27) or (args.max_frames and frame_count >= args.max_frames):
                    break
                if not args.no_display and cv2.getWindowProperty(window, cv2.WND_PROP_VISIBLE) < 1:
                    break
    except KeyboardInterrupt:
        status = "interrupted"
    except Exception as exc:
        status, error = "error", str(exc)
        raise
    finally:
        if capture is not None:
            capture.release()
        if not args.no_display:
            try:
                cv2.destroyAllWindows()
            except cv2.error:
                pass
        # ④ 성공/중단/오류 상태와 실제 측정값을 남깁니다. 측정하지 않은 정확도는 만들지 않습니다.
        summary = {
            "status": status, "error": error, "settings": config, "actual_device": device,
            "model_path": str(weight_path), "model_sha256": sha256(weight_path),
            "class_names": model.names, "actual_frame_size_wh": actual_size,
            "processed_frames": frame_count, "frames_with_detections": detected_frames,
            "total_detection_rows": detection_count, "snapshot_pairs": snapshot_count,
            "predict_call_mean_ms": float(np.mean(predict_times)) if predict_times else None,
            "predict_call_p95_ms": float(np.percentile(predict_times, 95)) if predict_times else None,
            "loop_fps": frame_count * 1000 / sum(loop_times) if sum(loop_times) > 0 else None,
            "run_seconds": time.perf_counter() - started, "warmup_calls_excluded": 2,
            "accuracy": None, "map50_95": None,
            "measurement_notes": {
                "predict_call_ms": "predict 호출 전후 경과시간: 전처리/추론/후처리 포함. CUDA는 동기화.",
                "loop_fps": "프레임 읽기/추론/그리기/표시/탐지행 기록/선택 캡처 포함. 초기화/최종 요약/frames.csv 쓰기 제외. 첫 프레임 읽기는 준비 중 수행.",
                "not_measured": "정답 라벨이 없으므로 정확도/mAP 미측정. FPS는 카메라 스펙이나 순수 모델 FPS가 아님.",
            },
            "environment": environment(),
        }
        write_json(output / "summary.json", summary)
        print(f"[종료] status={status}, frames={frame_count}, snapshots={snapshot_count}")
        print(f"[보고서 근거] {output / 'summary.json'}")
    return summary


if __name__ == "__main__":
    try:
        run(parse_args())
    except Exception as exc:
        print(f"[실행 실패] {exc}\n해결 안내: docs/TROUBLESHOOTING.md")
        raise SystemExit(1)
