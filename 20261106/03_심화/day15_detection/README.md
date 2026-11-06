# day15_detection · 실습 07~08
입력·출력을 구분한 모듈형 탐지·추적 프로젝트입니다. 실제 YOLO 설치와 `data/demo.pt`가 필요합니다.
모듈 역할: `vision.py`=model.predict/track와 표 변환, `main.py`=실행·저장, `restore.py`=새 프로세스 재현 대조.

## 실행
```powershell
python main.py
python restore.py
```

직접 완성: vision.py의 C07·C08, main.py의 C09, restore.py의 C10.
출력: `outputs/predictions.csv`, `image_counts.csv`, `tracks.csv`, `frames.csv`, `summary.json`, `tracked.avi`, `model.pt`.
PNG는 `outputs/images/`, 복원 PNG는 `outputs/restored_images/`입니다. 모델은 본인이 준비한 파일만 로드합니다.

실제 YOLO 미검증: 정상 처리 이미지12개·영상30프레임을 기대하지만, 검출 개수·ID·확률·속도는 실행 전 고정하지 않습니다.
빈 검출도 처리 이미지 수에 남깁니다. 복원 대조에서 같은 입력/클래스/행수와 좌표·확률 허용오차를 함께 확인합니다.
`reports/detection_report.md`에 모델 출처, 환경, 조건, 실패 사례, 성능 해석의 한계를 작성하세요.
Test는 호출하지 않습니다. 새 영상마다 새 Tracker 상태로 시작합니다. 사람의 정체성 식별이나 영상 간 ID 동일성 주장이 아닙니다.
