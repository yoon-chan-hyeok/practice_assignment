# 기본필수 · 수강생용

**Day13 | 처음 배우는 OpenCV | 코드 7개·정상 이미지3장·영상1개·README**

## 진행 원칙
함수·클래스·예외처리는 직접 작성하지 않습니다. TODO9곳만 완성합니다. 01~06은 서로 독립이며 앞 파일의 결과를 읽지 않습니다.
원본 이름은 scene.png·noisy.png·objects.png·sample.avi입니다. 결과는 p01_~p07_ 접두어로 같은 폴더에 생깁니다.
실행문이 끝나도 미완성 기본값이 남아 있을 수 있습니다. 코드의 TODO를 읽고, 아래 예상 결과·그림·설명 질문으로 확인합니다.

## 시작
수강생은 해당 TODO를 먼저 채운 뒤 실행합니다. 제공된 임시 값은 정답이 아닙니다.
[전체 환경 안내](../README.md)를 먼저 확인하고, 이 폴더에서 `python 01_read.py`를 실행합니다.
데이터는 320×240·uint8이며 결측·손상 파일이 없습니다. 필터를 위한 점 잡음은 정상 픽셀입니다.
제공된 os.chdir와 Path 코드는 경로 준비용입니다. 외우거나 다시 작성하지 않아도 됩니다.
GPU와 외부 다운로드는 필요 없습니다. PNG를 더블클릭하여 확인합니다.

| 실습 | 파일 | PPT | 직접 구현 |
|---|---|---:|---|
| 01 | [01_read.py](01_read.py) | 15 | B01 |
| 02 | [02_color_resize.py](02_color_resize.py) | 24 | B02 |
| 03 | [03_filter_edge.py](03_filter_edge.py) | 33 | B03 |
| 04 | [04_morphology.py](04_morphology.py) | 43 | B04 |
| 05 | [05_video.py](05_video.py) | 53 | B05 |
| 06 | [06_augment.py](06_augment.py) | 62 | B06 |
| 07 | [07_project.py](07_project.py) | 71 | B07, B08, B09 |
| 08 | 07번 파일 그대로 사용 | 77 | 추가 코드 없이 재실행·설명 |

## 실습 01 · 이미지 읽기·Shape·채널
scene.png를 읽고 배열·BGR 순서를 확인합니다. p01_copy.png는 원본 픽셀이 유지된 복사본입니다.

**열 파일:** `01_read.py` · PPT 15장

**B01 구현 지시**
scene.png를 cv2.imread로 읽어 image에 저장하세요. flags를 생략하면 BGR 컬러로 읽습니다.

### 함수·인자
`cv2.imread(filename, flags=cv2.IMREAD_COLOR)` — filename 필수, flags 선택. 반환은 NumPy 배열이며 읽기 실패 시 None입니다.
`cv2.imwrite(filename, image, params=[])` — 파일명·배열 필수, 압축 설정 선택. 반환은 저장 성공 bool입니다.

### 실행
```powershell
python 01_read.py
```

### 정답 실행 예
```text
shape: (240, 320, 3)
dtype: uint8
min/max: 0 255
빨강 패치의 BGR: [0, 0, 255]
PNG 저장: True
```

### 완료 기준·설명
shape의 (240,320,3)은 높이·너비·채널입니다. 빨강 패치의 BGR은 [0,0,255]입니다. dtype이 uint8인 이유를 설명하세요.

## 실습 02 · 색공간·Resize
Gray와 RGB를 구분하고 원본을 224×224로 축소합니다. RGB는 표시용이며 그대로 imwrite하지 않습니다.

**열 파일:** `02_color_resize.py` · PPT 24장

**B02 구현 지시**
image를 Gray와 RGB로 각각 변환하여 gray, rgb에 넣으세요. 두 번째 인자는 변환 코드입니다.

### 함수·인자
`cv2.cvtColor(src, code)` — 배열·변환 코드 모두 필수. 새 배열을 반환합니다.
`cv2.resize(src, dsize, interpolation=cv2.INTER_LINEAR)` — 여기서는 src·dsize=(W,H) 필수, interpolation 선택. INTER_AREA를 명시합니다.

### 실행
```powershell
python 02_color_resize.py
```

### 정답 실행 예
```text
Gray shape: (240, 320)
RGB 빨강: [255, 0, 0]
Resize shape: (224, 224, 3)
```

### 완료 기준·설명
Gray는 (240,320), 컬러 Resize는 (224,224,3)입니다. 4:3 이미지를 정사각형으로 만들면 모양이 변할 수 있습니다.

## 실습 03 · GaussianBlur·Canny
원본 noisy.png를 Gray로 바꾸고 필터 후 Edge를 구합니다. 커널과 두 임계값을 기록합니다.

**열 파일:** `03_filter_edge.py` · PPT 33장

**B03 구현 지시**
gray를 (5,5), sigmaX=0으로 흐리게 하여 blur를 만드세요. blur에 Canny 80,160을 적용하여 edge를 만드세요.

### 함수·인자
`cv2.GaussianBlur(src, ksize, sigmaX)` — 세 인자 필수. sigmaX=0이면 커널에서 계산. 선택 sigmaY=0, borderType=BORDER_DEFAULT입니다.
`cv2.Canny(image, threshold1, threshold2)` — 이 세 인자를 사용합니다. 선택 apertureSize=3, L2gradient=False. uint8 Edge를 반환합니다.

### 실행
```powershell
python 03_filter_edge.py
```

### 정답 실행 예
```text
설정: Gaussian (5,5), sigmaX=0, Canny 80/160
Shape: (240, 320) (240, 320)
Edge 픽셀: 3234
```

### 완료 기준·설명
blur와 edge는 같은 2D 크기입니다. Edge 픽셀이 많다고 좋은 결과는 아닙니다. 잡음 경계도 늘 수 있습니다.

## 실습 04 · Threshold·Opening
흰색을 전경으로 삼아 고정 임계값과 Opening을 적용합니다. 작은 흰 점과 작은 구멍의 차이를 관찰합니다.

**열 파일:** `04_morphology.py` · PPT 43장

**B04 구현 지시**
binary에 3×3 kernel을 사용한 Opening을 적용하세요. 결과 이름은 opened입니다.

### 함수·인자
`cv2.threshold(src, thresh, maxval, type)` — 네 인자 필수. (사용한 임계값, 결과 배열) 두 개를 반환합니다.
`cv2.morphologyEx(src, op, kernel, iterations=1)` — src·op·kernel 필수, iterations 선택. MORPH_OPEN은 침식→팽창입니다.

### 실행
```powershell
python 04_morphology.py
```

### 정답 실행 예
```text
임계값: 127.0
전경 픽셀: 14142 -> 14133
결과 값: [0, 255]
```

### 완료 기준·설명
값은 0과255입니다. Opening은 작은 흰 점을 줄일 수 있지만 검은 구멍을 모두 채우는 연산은 아닙니다. 구멍에는 Closing을 검토합니다.

## 실습 05 · 영상 Frame 처리
입력 영상 전체를 Gray로 변환해 저장하고 다시 읽습니다. 매 Frame은 같은 크기·채널로 Writer에 전달합니다.

**열 파일:** `05_video.py` · PPT 53장

**B05 구현 지시**
현재 frame을 Gray로 변환하여 gray에 넣으세요. VideoCapture는 반복문 밖에서 이미 열었습니다.

### 함수·인자
`cv2.VideoCapture(filename)` — 여기서는 filename 필수. read()는 (ok,frame), get(propId)는 메타데이터 값을 반환합니다.
`cv2.VideoWriter(filename, fourcc, fps, frameSize, isColor=True)` — 네 인자 필수, isColor 선택. frameSize는 (W,H). write(frame)는 bool이 아닌 None을 반환합니다.
`VideoWriter_fourcc(*"MJPG")`는 네 문자를 정수 코드로 만듭니다. release()는 별도 인자 없이 자원을 닫습니다.

### 실행
```powershell
python 05_video.py
```

### 정답 실행 예
```text
열림(입력/출력): True True
입력 FPS/크기: 12.0 (320, 240)
처리/재읽기 Frame: 48 48
재읽기 FPS: 12.0
```

### 완료 기준·설명
48frame·12fps·4초가 유지됩니다. Gray를 GRAY2BGR로 바꾸는 것은 컬러 복원이 아니라 3개 동일 채널로 만드는 것입니다.

## 실습 06 · 좌우반전·밝기
같은 그림에 좌우반전·밝기+30을 적용해 나란히 저장합니다. 원본은 수정하지 않습니다.

**열 파일:** `06_augment.py` · PPT 62장

**B06 구현 지시**
cv2.flip(image, 1)로 좌우 반전한 flipped를 만드세요. 세로 반전은 flipCode=0입니다.

### 함수·인자
`cv2.flip(src, flipCode)` — 두 인자 필수. 1=좌우, 0=상하, 음수=둘 다.
`np.clip(a, 0, 255)`는 범위를 제한합니다. uint8 상태로 +30을 하지 않고 float로 바꾼 뒤 처리합니다.
`cv2.hconcat([a,b,c])`는 높이·dtype이 같은 배열들을 가로로 잇습니다.

### 실행
```powershell
python 06_augment.py
```

### 정답 실행 예
```text
왼쪽 원본 / 가운데 좌우반전 / 오른쪽 +30 밝기
비교 그림 Shape: (240, 960, 3)
밝기 범위: 30 255
```

### 완료 기준·설명
비교 그림은 (240,960,3)입니다. 문자나 방향을 정답으로 쓰는 분류에서 좌우반전이 언제 부적절한지 설명하세요.

## 실습 07 · 이미지·영상 전처리 통합
정상 이미지3장과 영상1개를 Gray→Resize→Edge로 처리합니다. 08교시에 같은 코드를 다시 실행해 설명합니다.

**열 파일:** `07_project.py` · PPT 71장

**B07 구현 지시**
image를 Gray로 만든 뒤 (너비160, 높이120)으로 축소하세요. 변수는 gray, small입니다.

**B08 구현 지시**
축소한 small에 Canny 80,160을 적용하여 edge를 만드세요.

**B09 구현 지시**
각 frame에도 같은 Gray→160×120 Resize→Canny 순서를 적용하세요. 마지막 변수는 frame_edge입니다.

### 함수·인자
파일 입출력·반복문·CSV 저장 골격은 제공됩니다. 새 사용자 정의 함수나 예외처리를 만들지 않습니다.
`csv.writer(file)`의 writerow는 한 행, writerows는 여러 행을 기록합니다. 파일 open의 newline=""·encoding="utf-8-sig"는 제공 설정입니다.

### 실행
```powershell
python 07_project.py
```

### 정답 실행 예
```text
Writer: True
이미지 수/Frame 수: 3 48
재읽기 이미지 Shape: (120, 160)
재읽기 영상 Frame/FPS: 48 12.0
결과: p07_ PNG 9개 + AVI 1개 + CSV 1개
```

### 완료 기준·설명
이미지3장×3단계=PNG9개, 영상 AVI1개, CSV1개입니다. 출력160×120은 원본320×240과 같은 비율입니다.

## 실습08 · 같은 프로젝트 다시 실행하기
1. python 07_project.py를 다시 실행합니다. 새로운 08.py를 만들지 않습니다.
2. p07_summary.csv의 이미지3행과 저장 결과9개를 확인합니다. p07_video.avi의 재읽기 Frame48·FPS12를 확인합니다.
3. 원본과 결과를 나란히 열고 아래 세 문장을 직접 완성합니다.

- Gray 변환 후 달라진 정보는 ___이며, Resize가 바꾼 것은 ___입니다.
- Canny 결과에서 흰 픽셀은 ___을 의미합니다. 이것만으로 객체 탐지를 완료한 것은 아닙니다.
- 원본 보존·동일 재실행을 확인한 근거는 ___입니다.

## 막힐 때
- NoneType/shape 오류: B01이 아직 None인지, 입력 파일이 있는지, 실행 Python이 맞는지 확인합니다.
- 결과가 원본과 같다: 복사본 기본값이 남았는지 확인합니다. 실행 성공과 과제 완성은 다릅니다.
- 영상 열림 False/Frame0: 코덱·경로를 강사와 확인합니다. 비어있는 결과를 완료로 제출하지 않습니다.
- 모든 파일의 앞부분을 이해하지 못해도 TODO에 집중해도 됩니다. 강사는 파일구조나 검증코드 작성을 추가 요구하지 않습니다.

## 제출
완성한 Python7개, p07_ 결과11개, 이 README의 설명3문장. 원본4개는 변경하지 않습니다.
기본필수만으로 공통 평가를 완료할 수 있습니다. 검수용 자동 테스트·해시·병렬 구현은 요구하지 않습니다.

**예상 출력의 픽셀 개수는 검증 환경의 실제 결과입니다. 다른 OpenCV 빌드에서는 일부 경계가 달라질 수 있으므로, 설정·처리 순서와 이미지 의미를 함께 봅니다.**
