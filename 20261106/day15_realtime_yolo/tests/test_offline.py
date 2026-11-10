"""오프라인 회귀 검사. FakeModel은 로그 흐름 검사 전용이며 실제 YOLO 성능 검사가 아닙니다."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import cv2
import numpy as np
from PIL import Image
import torch
import yaml
import check_dataset as dataset
import main as webcam
import runtime
import train_custom
import evaluate_custom


class DataTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for split, color in [("train", "red"), ("val", "blue")]:
            (self.root / "images" / split).mkdir(parents=True)
            (self.root / "labels" / split).mkdir(parents=True)
            Image.new("RGB", (24, 24), color).save(self.root / "images" / split / "one.png")
            (self.root / "labels" / split / "one.txt").write_text("0 0.5 0.5 0.3 0.4\n")
        self.config = self.root / "data.yaml"
        self.config.write_text(yaml.safe_dump({"path": ".", "train": "images/train", "val": "images/val", "names": ["thing"]}))

    def test_valid_data(self):
        config, audit = dataset.audit_dataset(self.config)
        self.assertEqual(audit["summary"]["train"]["objects"], 1)
        self.assertEqual(config["val"], str(self.root / "images/val"))

    def test_placeholder_rejected(self):
        self.config.write_text("names: [CHANGE_ME]\n")
        with self.assertRaisesRegex(ValueError, "CHANGE_ME"):
            dataset.audit_dataset(self.config)

    def test_missing_label_rejected(self):
        (self.root / "labels/val/one.txt").unlink()
        with self.assertRaisesRegex(ValueError, "라벨 누락"):
            dataset.audit_dataset(self.config)

    def test_invalid_id_rejected(self):
        (self.root / "labels/val/one.txt").write_text("5 0.5 0.5 0.3 0.4\n")
        with self.assertRaisesRegex(ValueError, "class_id"):
            dataset.audit_dataset(self.config)

    def test_zero_width_rejected(self):
        (self.root / "labels/val/one.txt").write_text("0 0.5 0.5 0 0.4\n")
        with self.assertRaisesRegex(ValueError, "양수"):
            dataset.audit_dataset(self.config)

    def test_out_of_bounds_rejected(self):
        (self.root / "labels/val/one.txt").write_text("0 0.05 0.5 0.3 0.4\n")
        with self.assertRaisesRegex(ValueError, "이미지 밖"):
            dataset.audit_dataset(self.config)

    def test_cross_split_duplicate_rejected(self):
        (self.root / "images/val/one.png").write_bytes((self.root / "images/train/one.png").read_bytes())
        with self.assertRaisesRegex(ValueError, "동일 중복"):
            dataset.audit_dataset(self.config)

    def test_empty_background_allowed(self):
        Image.new("RGB", (24, 24), "green").save(self.root / "images/train/background.png")
        (self.root / "labels/train/background.txt").write_text("")
        _, audit = dataset.audit_dataset(self.config)
        self.assertEqual(audit["summary"]["train"]["background_images"], 1)

    def test_test_split_not_read(self):
        raw = yaml.safe_load(self.config.read_text())
        raw["test"] = "images/test"
        self.config.write_text(yaml.safe_dump(raw))
        (self.root / "images/test").mkdir()
        (self.root / "images/test/broken.png").write_bytes(b"not-an-image")
        _, audit = dataset.audit_dataset(self.config)
        self.assertNotIn("test", audit["summary"])

    def test_other_folder_layout(self):
        source = Path("/tmp/custom/train/images/abc.jpg")
        self.assertEqual(dataset.label_path(source), Path("/tmp/custom/train/labels/abc.txt"))

    def test_train_wrapper_mock(self):
        # 학습 API 호출 인자/폴더/최신 모델 포인터 연결만 검사합니다.
        output = self.root / "outputs/train_mock"
        output.mkdir(parents=True)
        capture = {}
        class FakeTrainerModel:
            def train(self, **kwargs):
                capture.update(kwargs)
                self.trainer = SimpleNamespace(save_dir=output)
                (output / "weights").mkdir()
                for name in ("best.pt", "last.pt"):
                    (output / "weights" / name).write_bytes(b"mock checkpoint, NOT real weights")
        with patch.object(train_custom, "BASE", self.root), \
             patch.object(train_custom, "new_run_dir", return_value=output), \
             patch.object(train_custom, "load_detector", return_value=(FakeTrainerModel(), self.root / "base.pt")), \
             patch.object(sys, "argv", ["train_custom.py", "--data", str(self.config), "--epochs", "1", "--device", "cpu"]):
            train_custom.main()
        active = yaml.safe_load(Path(capture["data"]).read_text())
        self.assertNotIn("test", active)
        self.assertEqual(capture["workers"], 0)
        self.assertEqual(capture["epochs"], 1)
        pointer = json.loads((self.root / "outputs/latest_custom.json").read_text())
        self.assertEqual(pointer["best_pt"], "outputs/train_mock/weights/best.pt")

    def test_eval_wrapper_mock(self):
        output = self.root / "outputs/eval_mock"
        output.mkdir(parents=True)
        capture = {}
        box = SimpleNamespace(mp=.5, mr=.6, map50=.4, map=.2, ap_class_index=[0],
                              class_result=lambda i: (.5, .6, .4, .2))
        class FakeEvaluatorModel:
            names = {0: "thing"}
            def val(self, **kwargs):
                capture.update(kwargs)
                return SimpleNamespace(box=box)
        with patch.object(evaluate_custom, "BASE", self.root), \
             patch.object(evaluate_custom, "new_run_dir", return_value=output), \
             patch.object(evaluate_custom, "load_detector", return_value=(FakeEvaluatorModel(), self.root / "best.pt")), \
             patch.object(sys, "argv", ["evaluate_custom.py", "--data", str(self.config), "--device", "cpu"]):
            evaluate_custom.main()
        self.assertEqual(capture["split"], "val")
        self.assertEqual(capture["conf"], .001)
        saved = json.loads((output / "metrics.json").read_text())
        self.assertEqual(saved["map50_95"], .2)

    def test_eval_rejects_class_mismatch(self):
        fake = SimpleNamespace(names={0: "wrong-class"})
        with patch.object(evaluate_custom, "load_detector", return_value=(fake, self.root / "best.pt")), \
             patch.object(sys, "argv", ["evaluate_custom.py", "--data", str(self.config)]):
            with self.assertRaisesRegex(ValueError, "클래스"):
                evaluate_custom.main()


class VideoTests(unittest.TestCase):
    def test_original_demo_readable(self):
        cap = cv2.VideoCapture(str(ROOT / "assets/day15_demo.avi"))
        count = 0
        try:
            self.assertTrue(cap.isOpened())
            while True:
                ok, frame = cap.read()
                if not ok:
                    break
                self.assertEqual(frame.shape, (128, 160, 3))
                count += 1
        finally:
            cap.release()
        self.assertEqual(count, 30)

    def test_frame_loop_logs_and_snapshots_with_mock(self):
        # 실제 OpenCV 영상 디코딩/PNG 인코딩/CSV 쓰기를 실행합니다.
        # YOLO 부분만 FakeModel로 대체합니다. 검출 성능/속도를 평가하지 않습니다.
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            output = folder / "run"
            output.mkdir()
            class FakeModel:
                names = {0: "mock-object"}
                calls = 0
                def predict(self, frame, **kwargs):
                    self.calls += 1
                    n = int(self.calls % 2 == 1)
                    boxes = SimpleNamespace(xyxy=torch.tensor([[1., 2., 20., 22.]] * n).reshape(n, 4),
                                            conf=torch.tensor([.9] * n), cls=torch.tensor([0] * n))
                    return [SimpleNamespace(boxes=boxes, names=self.names, plot=lambda: frame.copy())]
            args = argparse.Namespace(model=None, source=str(ROOT / "assets/day15_demo.avi"),
                                      device="cpu", conf=None, imgsz=None, no_display=True,
                                      max_frames=6, snapshot_every=2)
            with patch.object(webcam, "load_detector", return_value=(FakeModel(), folder / "mock.pt")), \
                 patch.object(webcam, "new_run_dir", return_value=output):
                summary = webcam.run(args)
            self.assertEqual(summary["processed_frames"], 6)
            self.assertEqual(summary["total_detection_rows"], 3)
            self.assertEqual(summary["snapshot_pairs"], 3)
            self.assertIsNone(summary["map50_95"])
            self.assertEqual(len(list((output / "snapshots").glob("*.png"))), 6)
            with (output / "frames.csv").open(encoding="utf-8-sig") as file:
                rows = list(csv.DictReader(file))
            self.assertEqual(len(rows), 6)
            self.assertIn("0", [r["detections"] for r in rows])
            self.assertEqual(json.loads((output / "summary.json").read_text())["status"], "completed")


if __name__ == "__main__":
    unittest.main(verbosity=2)
