"""라벨 감사: 빈 라벨을 정상 negative로 다루고, 누락은 따로 표시한다."""
from pathlib import Path
import hashlib, csv
from PIL import Image
import numpy as np
from geometry import Box


def audit_label(label_path,width,height,names):
    # >>> X06
    # 요구: UTF-8 YOLO TXT 한 줄=class cx cy w h. 공백 줄은 무시한다.
    # 각 줄의 열 수5, class 정수/범위, 유한수, 중심·크기·유도 경계 검사를 한다.
    # 완전 중복 라벨은 오류. 빈 파일은 objects=0, errors=[]인 정상 negative.
    # 없는 파일은 missing_label 오류(운영 계약). 잘못된 줄은 line 번호를 남긴다.
    # 반환 {objects:int, errors:list[str]}; 원본을 수정/자동 clip/삭제하지 않는다.
    raise NotImplementedError("TODO X06를 구현하세요.")
    # <<< X06


def audit_dataset(data):
    data=Path(data);rows=[];hashes={};groups={};issues=[]
    with (data/'manifest.csv').open(encoding='utf-8-sig',newline='') as f:
        manifest=list(csv.DictReader(f))
    for m in manifest:
        p=data/m['image']
        with Image.open(p) as im: width,height=im.size;im.verify()
        label=audit_label(data/m['label'],width,height,['square','circle','triangle'])
        sha=hashlib.sha256(p.read_bytes()).hexdigest()
        for old in hashes.get(sha,[]):
            if old['split']!=m['split']:issues.append('cross_split_duplicate:'+old['image_id']+':'+m['image_id'])
        hashes.setdefault(sha,[]).append(m)
        groups.setdefault(m['group_id'],set()).add(m['split'])
        rows.append(dict(image_id=m['image_id'],split=m['split'],objects=label['objects'],errors=';'.join(label['errors']),sha256=sha))
    for group,splitset in groups.items():
        if len(splitset)>1:issues.append('cross_split_group:'+group)
    return rows,issues
