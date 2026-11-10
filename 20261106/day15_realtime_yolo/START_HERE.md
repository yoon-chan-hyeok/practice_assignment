# Day15 · 1시간 실시간 YOLO 프로젝트

**오늘 할 일: 실행 → 조건 변경 → 증빙 저장 → 짧은 보고서. 추가 학습은 선택입니다.**

## 1. 실행 준비

ZIP을 **압축 해제**하고 이 폴더를 VS Code로 여세요. 기존 Day15 가상환경의 Python을 선택합니다. PowerShell/터미널에서 아래 명령을 실행하세요.

```powershell
# 기존 환경에 패키지가 모두 있으면 설치 명령은 생략 가능합니다.
python -m pip install -r requirements.txt

# 최초 1회: 패키지/모델 준비. 인터넷 연결이 필요합니다.
python check_setup.py

# 기본 필수: 카메라 실시간 탐지
python main.py
```

사전학습 가중치 `yolo26n.pt`는 ZIP에 포함되어 있지 않습니다. 최초 실행 때 공식 가중치를 다운로드하여 `weights/`에 저장합니다. 강사가 수업 전에 이 파일을 준비하면 학생은 가중치 다운로드 없이 실행할 수 있습니다. Python 패키지는 별도로 설치되어 있어야 합니다.

## 2. 조작

영상 창을 클릭한 뒤 **S**를 누르면 보고서용 원본·탐지 화면이 함께 저장됩니다. **Q 또는 ESC**로 종료합니다. 기본 설정은 녹화하지 않으며 카메라 영상을 업로드하는 기능을 넣지 않았습니다. 얼굴·이름표·모니터 내용 등 개인정보가 포함된 캡처는 제출하지 마세요.

## 3. 필수 과제

| 순서 | 수행 내용 | 완료 기준 |
|---|---|---|
| 1 | 컵·병·책·휴대전화 등 모델에 정의된 물체를 카메라에 제시 | 박스/클래스/점수가 표시되는지 관찰 |
| 2 | 거리 또는 가림을 바꾸어 관찰 | 조건 3개 기록, 증빙 캡처 2장 이상 |
| 3 | confidence를 한 번 변경하여 비교 | 기본 0.25와 변경 0.60 비교 |
| 4 | 보고서 작성 | `reports/REPORT_TEMPLATE.md`를 복사해 1~2페이지 작성 |

```powershell
python main.py --conf 0.60
```

같은 모델·장치·입력 크기를 유지하고 같은 물체/환경에서 비교하세요. 실시간 장면이 완전히 같지 않으므로 엄밀한 통제실험이라는 주장은 하지 않습니다. 오류를 못 보았다면 **“관찰 범위에서 오류 미관찰”**로 기록하고 사례를 만들지 않습니다.

## 4. 결과 위치

각 실행마다 `outputs/webcam_날짜_시간/`이 새로 생깁니다. `summary.json`은 설정/시간, `snapshots/`는 증빙, `detections.csv`는 프레임별 탐지입니다. **confidence는 정확도가 아니며, 기본 웹캠 실습의 mAP는 ‘미측정’입니다.**

## 5. 문제가 생기면

```powershell
python main.py --source 1       # 다른 카메라 번호
python main.py --device cpu     # GPU 환경 문제 시
python main.py --imgsz 256      # 입력 크기를 낮춰 속도 비교
```

카메라가 없으면 `python main.py --source assets/day15_demo.avi`로 입출력 흐름을 확인할 수 있습니다. 이 파일은 기존 Day15의 **도형 합성 영상**이며 기본 COCO 사전학습 모델의 탐지 품질을 평가하는 자료가 아닙니다. 실제 물체 영상이 있다면 `--source "내영상.mp4"`로 대체하세요.

**선택 과제: `datasets/custom/README.md`를 읽고 새 데이터 준비 → `check_dataset.py` → `train_custom.py` → `evaluate_custom.py` → `main.py --model custom` 순서로 진행합니다.**
