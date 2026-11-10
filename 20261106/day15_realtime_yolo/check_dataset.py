"""선택 과제의 데이터 점검: 경로/라벨/클래스/좌표/바이트 중복. 기본 train·val만 읽습니다."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path
import hashlib
import math

import yaml
from PIL import Image
from runtime import BASE, project_path, write_json

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def load_config(data_file: str | Path) -> dict:
    """상대 path는 YAML 위치 기준. Ultralytics에는 절대경로로 변환해 전달합니다."""
    file = project_path(data_file)
    config = yaml.safe_load(file.read_text(encoding="utf-8-sig"))
    if not isinstance(config, dict):
        raise ValueError("data.yaml은 사전 형태여야 합니다.")
    names = config.get("names")
    if isinstance(names, dict):
        try:
            mapping = {int(k): str(v) for k, v in names.items()}
        except (ValueError, TypeError) as exc:
            raise ValueError("names의 키는 0부터 시작하는 클래스 ID여야 합니다.") from exc
        if sorted(mapping) != list(range(len(mapping))):
            raise ValueError("클래스 ID는 0, 1, 2, ...처럼 연속이어야 합니다.")
        names = [mapping[i] for i in range(len(mapping))]
    if not isinstance(names, list) or not names or any(not isinstance(n, str) or not n.strip() for n in names):
        raise ValueError("names에 실제 클래스 이름을 입력하세요.")
    if len(set(names)) != len(names) or "CHANGE_ME" in names:
        raise ValueError("data.yaml의 CHANGE_ME를 실제 클래스 이름으로 바꾸세요. 클래스 이름은 중복할 수 없습니다.")
    root = Path(str(config.get("path", "."))).expanduser()
    root = root.resolve() if root.is_absolute() else (file.parent / root).resolve()
    active = {"path": str(root), "names": names}
    for split in ("train", "val", "test"):
        value = config.get(split)
        if value:
            if not isinstance(value, str):
                raise ValueError("이 최소 프로젝트는 split별 이미지 폴더 하나를 지원합니다.")
            path = Path(value)
            active[split] = str(path.resolve() if path.is_absolute() else (root / path).resolve())
    return active


def label_path(image_path: Path) -> Path:
    # images/train/a.png → labels/train/a.txt
    # train/images/a.png → train/labels/a.txt 구조도 지원합니다.
    parts = list(image_path.parts)
    indices = [i for i, value in enumerate(parts) if value == "images"]
    if not indices:
        raise ValueError(f"이미지 경로에 images 폴더가 필요합니다: {image_path}")
    parts[indices[-1]] = "labels"
    return Path(*parts).with_suffix(".txt")


def audit_dataset(data_file: str | Path, splits=("train", "val")) -> tuple[dict, dict]:
    config = load_config(data_file)
    issues, warnings, summary = [], [], {}
    seen = defaultdict(list)
    for split in splits:
        folder = Path(config.get(split, ""))
        if split not in config or not folder.is_dir():
            issues.append(f"{split}: 이미지 폴더가 없거나 YAML에 지정되지 않았습니다: {config.get(split)}")
            continue
        images = sorted(p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS)
        if not images:
            issues.append(f"{split}: 이미지가 없습니다: {folder}")
        counts, background = Counter(), 0
        used_labels = set()
        for image in images:
            try:
                with Image.open(image) as source:
                    source.verify()
            except Exception as exc:
                issues.append(f"이미지 읽기 실패: {image.name}: {exc}")
                continue
            digest = hashlib.sha256(image.read_bytes()).hexdigest()
            seen[digest].append((split, str(image)))
            label = label_path(image)
            if label in used_labels:
                issues.append(f"여러 이미지가 같은 라벨 파일을 공유합니다: {label}")
            used_labels.add(label)
            if not label.is_file():
                # 공식 로더보다 엄격한 교육용 정책: 배경은 빈 TXT로 명시합니다.
                issues.append(f"라벨 누락: {label}. 배경 이미지라면 빈 TXT를 명시적으로 만드세요.")
                continue
            lines = label.read_text(encoding="utf-8-sig").splitlines()
            nonempty = [line for line in lines if line.strip()]
            if not nonempty:
                background += 1
            for line_no, line in enumerate(lines, 1):
                if not line.strip():
                    continue
                try:
                    values = [float(v) for v in line.split()]
                    if len(values) != 5 or not all(math.isfinite(v) for v in values):
                        raise ValueError("정상 숫자 5개(class cx cy w h)가 필요합니다.")
                    cls, cx, cy, w, h = values
                    if not cls.is_integer() or not 0 <= cls < len(config["names"]):
                        raise ValueError("class_id가 names 범위를 벗어납니다.")
                    if not (0 <= cx <= 1 and 0 <= cy <= 1 and 0 < w <= 1 and 0 < h <= 1):
                        raise ValueError("좌표는 정규화 값, 너비/높이는 양수여야 합니다.")
                    eps = 1e-4
                    if cx - w/2 < -eps or cy - h/2 < -eps or cx + w/2 > 1+eps or cy + h/2 > 1+eps:
                        raise ValueError("박스 경계가 이미지 밖에 있습니다. 라벨을 확인하세요.")
                    counts[int(cls)] += 1
                except ValueError as exc:
                    issues.append(f"{label.name}:{line_no}: {exc}")
        if images and sum(counts.values()) == 0:
            issues.append(f"{split}: 유효한 정답 박스가 0개입니다.")
        missing_classes = [config["names"][i] for i in range(len(config["names"])) if counts[i] == 0]
        if missing_classes:
            warnings.append(f"{split}에 없는 클래스: {missing_classes}. 해당 클래스 성능을 주장하지 마세요.")
        summary[split] = {"images": len(images), "objects": sum(counts.values()), "background_images": background,
                          "class_counts": {config["names"][i]: counts[i] for i in range(len(config["names"]))}}
    duplicate_groups = [items for items in seen.values() if len(items) > 1]
    cross_split = [items for items in duplicate_groups if len({split for split, _ in items}) > 1]
    if cross_split:
        issues.append(f"서로 다른 split 사이에 바이트 동일 중복 그룹 {len(cross_split)}개가 있습니다.")
    elif duplicate_groups:
        warnings.append(f"동일 split 내부 바이트 중복 그룹 {len(duplicate_groups)}개가 있습니다.")
    audit = {"checked_splits": list(splits), "summary": summary, "warnings": warnings,
             "issues": issues, "duplicate_groups": duplicate_groups,
             "limitation": "픽셀/시각적 유사도, 연속 프레임 누수, 실제 박스 정확성은 자동 검증하지 않음."}
    if issues:
        raise ValueError("데이터 점검 실패:\n- " + "\n- ".join(issues[:20]) + ("\n(이하 생략)" if len(issues) > 20 else ""))
    return config, audit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default="datasets/custom/data.yaml")
    args = parser.parse_args()
    config, audit = audit_dataset(args.data)
    path = BASE / "outputs/custom_dataset_audit.json"
    write_json(path, audit)
    print("[PASS] 데이터 경로/라벨 기본 점검 완료")
    print(audit["summary"])
    for warning in audit["warnings"]:
        print("[주의]", warning)
    print("증빙:", path)
    print("Test는 읽지 않았습니다. 박스가 실제 물체를 감싸는지 별도 시각 점검하세요.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(exc)
        raise SystemExit(1)
