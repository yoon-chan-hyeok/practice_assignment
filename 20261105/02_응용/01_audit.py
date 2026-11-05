"""Day14: 제공된 정상 이미지로 학습합니다. test는 읽지 않습니다."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import torch
from torch import nn
from torchvision.datasets import ImageFolder
from torchvision import transforms as tr
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix

torch.set_num_threads(1)
torch.manual_seed(14)
BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

# 여기서는 [0,1] RGB 32×32로 학습한 교육용 source 가중치를 사용합니다.
# ImageNet ResNet18과 입력 변환을 섞지 않습니다.
transform = tr.Compose([tr.Resize((32, 32)), tr.ToTensor()])
from collections import defaultdict
import hashlib
rows = []
seen = defaultdict(list)
for split in ["train", "valid", "test"]:
    dataset = ImageFolder(DATA / split)
    for label, name in enumerate(dataset.classes):
        # TODO A01: 해당 라벨의 개수를 세세요.
        # BEGIN A01
        count = 0  # dataset.targets에서 label의 수를 세세요.
        # END A01
        rows.append({"split": split, "class": name, "n": count, "ratio": count/len(dataset)})
    for path,_ in dataset.samples:
        seen[hashlib.sha256(Path(path).read_bytes()).hexdigest()].append(str(Path(path).relative_to(DATA)))
table = pd.DataFrame(rows)
table.to_csv(OUT/"class_counts.csv", index=False)
print(table.round(4).to_string(index=False))
duplicates = [paths for paths in seen.values() if len(paths)>1]
print("바이트 동일 중복 그룹:",len(duplicates))
(OUT/"duplicates.json").write_text(json.dumps(duplicates,ensure_ascii=False,indent=2),encoding="utf-8")
# test 픽셀은 중복 감사에만 쓰며 모델 성능을 계산하지 않습니다.
