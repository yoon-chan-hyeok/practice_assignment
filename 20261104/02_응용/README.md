# 응용 · data와 outputs를 나누어 처리하기

기본필수 후 선택 경로입니다. TODO8곳, 코드7개, data/와 outputs/의 얕은 구조입니다.
각 파일은 독립 실행되며 07에서 통합하고 08에서 같은 결과를 확인합니다. 코드의 함수는 증강1개와 프로젝트2개로 제한했습니다.
입력은 data/에서 읽고, 생성 파일은 outputs/에만 저장합니다. outputs/는 코드가 자동으로 만듭니다.
[환경 안내](../README.md)에서 같은 venv·패키지를 먼저 확인하세요.

## 실습01 · BGR/RGB와 채널 평균
**파일:** [01_channels.py](01_channels.py) · PPT 15장 · TODO A01

**A01:** Matplotlib 표시 전에 BGR을 RGB로 변환하세요. 원본 image는 그대로 유지합니다.

함수·처리 주의: cv2.cvtColor의 src/code 필수. mean(axis=(0,1))은 공간 축 두 개를 평균냅니다. Matplotlib imshow는 RGB로 해석합니다.

```powershell
python 01_channels.py
```

정답 실행 예:
```text
BGR 채널평균: [111.002, 124.354, 118.358]
변환후 빨강: [255, 0, 0]
```

완료 기준: 두 PNG의 빨강/파랑 차이와 CSV 채널 순서를 확인합니다.

## 실습02 · 보간법 비교
**파일:** [02_interpolation.py](02_interpolation.py) · PPT 24장 · TODO A02

**A02:** 현재 method를 사용해 (너비80, 높이60)으로 축소한 small을 만드세요.

함수·처리 주의: resize의 interpolation은 선택 인자이며 기본 LINEAR입니다. 이 실습에서는 NEAREST/LINEAR/AREA를 명시합니다.

```powershell
python 02_interpolation.py
```

정답 실행 예:
```text
[['nearest', 80, 60, 723.4032], ['linear', 80, 60, 304.8467], ['area', 80, 60, 335.436]]
왕복 MSE는 이 합성 이미지의 수치 비교이며 모델 성능이 아닙니다.
```

완료 기준: 세 후보를 같은 원본·같은80×60에서 비교합니다. 확대 후 정보가 복구되었다고 주장하지 않습니다.

## 실습03 · 필터와 Edge
**파일:** [03_filters.py](03_filters.py) · PPT 33장 · TODO A03

**A03:** 같은 gray에 Gaussian (5,5), sigmaX=0과 Median ksize=5를 각각 적용하세요.

함수·처리 주의: medianBlur(src,ksize)는 두 인자 필수. ksize=5는 양의 홀수입니다.

```powershell
python 03_filters.py
```

정답 실행 예:
```text
[['original', 11507], ['gaussian', 3234], ['median', 2582]]
Edge가 많다고 무조건 좋지 않습니다. 잡음 경계일 수도 있습니다.
```

완료 기준: 필터별 Edge 수를 기록하고 잡음이 경계를 늘리는지 관찰합니다.

## 실습04 · 고정 임계값과 Otsu
**파일:** [04_thresholds.py](04_thresholds.py) · PPT 43장 · TODO A04

**A04:** Otsu로 임계값을 자동 결정하세요. 반환값 두 개를 otsu_t와 otsu로 받습니다.

함수·처리 주의: threshold는 (retval,dst)를 반환합니다. OTSU 플래그에서 thresh=0은 직접 정한 임계값을 쓰지 않는 자리입니다.

```powershell
python 04_thresholds.py
```

정답 실행 예:
```text
[['fixed', 127.0, 38302, 38334], ['otsu', 116.0, 42113, 42149]]
```

완료 기준: Otsu가 선택한 threshold를 함께 기록하고 전경 증가가 반드시 개선은 아닌 이유를 적습니다.

## 실습05 · Frame 샘플링
**파일:** [05_video_sampling.py](05_video_sampling.py) · PPT 53장 · TODO A05

**A05:** 매 every번째 frame만 저장해도 원래 재생시간을 유지하도록 output_fps를 계산하세요. 이 입력은 48이 1·3으로 나누어떨어집니다.

함수·처리 주의: wall_s는 decode·처리·write를 포함합니다. processed_fps는 저장한 Frame 수/wall_s이며 원본 동영상의 재생 FPS와 다릅니다.

```powershell
python 05_video_sampling.py
```

정답 실행 예:
```text
N=1: 읽기48, 저장48, fps=12.0, 출력초=4.00
N=3: 읽기48, 저장16, fps=4.0, 출력초=4.00
시간은 decode+처리+encode 포함. 모든 입력은 decode하므로 N배 가속을 보장하지 않습니다.
```

완료 기준: N=1은48frame/12fps, N=3은16frame/4fps로 모두4초입니다. 모든 Frame을 decode하는 범위임을 기록합니다.

## 실습06 · Seed를 사용하는 작은 함수
**파일:** [06_seed_augmentation.py](06_seed_augmentation.py) · PPT 62장 · TODO A06

**A06:** float32에서 beta를 더하고 [0,255]로 clip한 뒤 uint8로 돌리세요. uint8 상태로 직접 더하지 않습니다.

함수·처리 주의: default_rng(seed)의 seed는 선택 인자지만 여기서는 명시합니다. 로컬 Generator를 사용하며 전역 난수를 재설정하지 않습니다.

```powershell
python 06_seed_augmentation.py
```

정답 실행 예:
```text
같은 seed 결과 일치: True
설정: {'seed': 42, 'flip': False, 'beta': 8}
```

완료 기준: 같은 seed42로 동일한 결과를 얻습니다. 원본과 두 결과를 비교합니다.

## 실습07 · 이미지·영상 처리 함수 연결
**파일:** [07_project.py](07_project.py) · PPT 71장 · TODO A07·A08

**A07:** Gray→160×120 Resize→3×3 Gaussian→Canny 80/160을 구현하세요. 반환 변수 gray·small·edge를 만듭니다.

**A08:** process_image(frame)의 세 번째 반환값 edge를 받아 3채널 BGR로 변환해 반환하세요.

함수·처리 주의: process_image(image)는 gray/small/edge를 반환합니다. process_frame(frame)은 Writer용3채널 결과만 반환합니다. 두 함수에서 파일을 새로 열지 않습니다.

```powershell
python 07_project.py
```

정답 실행 예:
```text
이미지 처리표: 9 행 / 원본3장
Frame 처리/재읽기: 48 48
재읽기 크기/FPS: 160 120 12.0
PNG 저장·재읽기 모두 일치: True
```

완료 기준: 이미지3장의 단계별 결과9개와 비교 PNG3개, 영상1개, 요약CSV를 만듭니다.

## 실습08 · 짝과 재현 확인
python 07_project.py를 같은 설정으로 재실행합니다. result_summary.csv는9행, PNG 재읽기는 모두 True, 영상 Frame48·160×120·FPS12를 확인합니다.
측정시간은 매번 달라도 됩니다. 픽셀·설정·파일수와 동작이 같은지를 구분합니다.

### 설명 작성
- 입력과 출력 경로를 나눈 이유: ___
- 모든 Frame decode와 매N번째 Frame 처리의 차이: ___
- 원본 FPS로 16frame만 저장했다면 왜 재생시간이 달라지는가: ___
- 같은 seed가 라벨 보존을 보장하지 않는 이유: ___

### 제출
완성 코드7개, outputs/result_summary.csv와 p07_ 결과, README의 설명. 함수·폴더를 추가로 늘릴 필요는 없습니다.
CSV 시간은 환경 의존적이며 학생의 성능 순위를 정하는 자료가 아닙니다.
