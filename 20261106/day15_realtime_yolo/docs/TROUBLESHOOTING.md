# 실행 문제 해결

## 카메라가 안 열린다 / 검은 화면

Windows의 카메라 권한과 물리 셔터를 확인하세요. 카메라를 사용하는 다른 앱을 종료하고 재시도합니다. 다음 명령으로 다른 장치 번호를 확인할 수 있습니다.

```powershell
python check_setup.py --camera 0
python main.py --source 1
```

이 프로그램은 Windows에서 DirectShow를 먼저 시도하고 실패하면 기본 백엔드로 재시도합니다. 열기는 성공하지만 프레임 읽기에 실패할 때는 장치 번호·권한·드라이버를 점검하세요. 기본 자동 재시도가 모든 장치를 지원하는 것은 아닙니다.

카메라 자체가 없으면 허가받은 실제 물체 영상으로 대체합니다.

```powershell
python main.py --source "C:/videos/my_objects.mp4"
```

포함된 `assets/day15_demo.avi`는 도형 영상이므로 기본 모델의 일상 물체 탐지 성능을 확인하는 자료가 아닙니다.

## ModuleNotFoundError / VS Code에서는 패키지가 없다

```powershell
python -c "import sys; print(sys.executable)"
python -m pip install -r requirements.txt
python check_setup.py
```

VS Code에서 선택한 Python과 위 경로를 맞추세요. 기존 GPU용 torch가 정상이라면 무작정 재설치하지 않습니다.

## yolo26n.pt가 없다 / 다운로드 실패

처음 한 번은 인터넷이 필요합니다. 공식 가중치 파일을 받아 `weights/yolo26n.pt`에 놓으면 해당 파일을 재사용합니다. 설정을 `yolo26n.yaml`로 바꾸면 사전학습 모델이 아니라 초기화 구조가 되므로 해결책이 아닙니다. 신뢰할 수 없는 `.pt`는 로드하지 마세요.

YOLO26 관련 클래스/구조를 인식하지 못하는 오류면 현재 Python의 ultralytics 버전과 수업 환경을 먼저 비교합니다. 패키지를 업데이트할 때는 강사가 점검한 환경을 사용하세요.

## GPU 오류 / 메모리 부족

```powershell
python main.py --device cpu
python main.py --imgsz 256
python train_custom.py --device cpu --batch 1 --imgsz 256 --epochs 2
```

CUDA 사용 가능 여부는 `check_setup.py`에서 출력합니다. GPU가 있어도 CPU용 PyTorch 환경이면 기본 동작은 CPU입니다. GPU를 사용하면 반드시 특정 FPS가 나온다고 보장하지 않습니다.

## cv2.imshow 관련 오류 / 창이 뜨지 않는다

로컬 VS Code/터미널에서 실행해야 합니다. Colab/원격 서버의 `source=0`은 사용자의 노트북 카메라가 아닙니다. GUI 없는 OpenCV 패키지를 쓰는 환경에서는 창이 표시되지 않을 수 있습니다.

```powershell
python -m pip show opencv-python opencv-python-headless opencv-contrib-python opencv-contrib-python-headless
```

같은 환경에 여러 변형이 설치되어 있으면 강사와 상의하여 정리하고 GUI 지원 패키지를 사용하세요. 무작정 모든 OpenCV 패키지를 지우는 자동 정리 코드는 제공하지 않습니다. 서버 자동 점검은 영상 파일과 `--no-display --max-frames 30`을 사용합니다.

## 박스가 하나도 안 보인다

먼저 모델의 클래스 목록(`weights/classes.json`)에 해당 물체가 있는지 봅니다. 물체를 밝은 곳에 크게 제시하고 `--conf 0.10` 또는 `--imgsz 640`으로 비교할 수 있습니다. 단, 낮은 threshold는 오탐을 늘릴 수 있으며 좋은 성능을 보장하지 않습니다. 기존 smoke 모델/합성 도형 모델을 일상 물체용 모델로 착각하지 마세요.

## S/Q를 눌러도 반응이 없다

터미널이 아니라 **영상 창을 클릭한 뒤** 키를 누릅니다. 한 프레임 추론이 오래 걸리면 입력 반영도 늦을 수 있습니다. 터미널 Ctrl+C도 정리/요약 저장을 시도하지만 강제 프로세스 종료나 전원 차단에서는 요약 저장을 보장하지 않습니다.

## 학습 이미지 경로가 없다

실제 폴더가 `images/valid`이면 YAML은 `val: images/valid`로 지정합니다. `val` 키 자체를 `valid`로 바꾸지 않습니다. `train/images` 구조이면 값도 `train/images`로 적습니다. 프로그램이 생성한 `dataset_active.yaml`을 확인하세요.

## 데이터 점검이 CHANGE_ME / 라벨 누락 / 클래스 오류로 중단된다

실제 데이터가 없는 템플릿이므로 정상적인 보호 동작입니다. 이미지와 YOLO TXT 라벨을 준비하고 클래스 ID 순서에 맞게 names를 수정하세요. 객체가 있지만 라벨이 없는 이미지를 빈 TXT로 만들면 안 됩니다. 경계 좌표는 절대 픽셀이 아니라 정규화된 중심/크기입니다.

## evaluate_custom.py가 모델 클래스가 다르다고 한다

올바른 best.pt와 학습 때의 data.yaml을 사용하세요. 예를 들어 COCO 클래스 0은 사용자 데이터 클래스 0과 의미가 다를 수 있습니다. 이름만 바꾸거나 검사를 제거하는 것은 해결이 아닙니다.

## 이전 학습과 이번 학습이 섞인다

각 실험은 시간 이름의 새 폴더에 저장됩니다. `--model custom`은 가장 최근 성공한 추가 학습 모델이므로 특정 실행을 재현할 때는 `.pt` 경로를 명시하세요. 스크립트 재실행으로 학습이 자동 누적되지 않습니다. 이 자료는 `resume`을 자동 적용하지 않습니다.
