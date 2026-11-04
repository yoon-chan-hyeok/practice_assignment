# HSV Mask·Letterbox

PPT 24장에 대응합니다. 구현 난이도는 기존 응용 수준입니다.

## 파일 역할
main.py에서 시작합니다. shared ../data는 원본이며 outputs/는 실행으로 생성됩니다. filters.py·video_ops.py가 있는 단원은 계산을 그 모듈에 둡니다.

## 구현할 부분
### H02 · `main.py`
new_w·new_h로 Resize한 뒤 top/bottom/left/right 여백을 추가해 size와 같은 크기를 만드세요. result에 저장합니다.

## 실행
현재 단원 폴더에서 다음을 실행합니다. 절대 경로로 main.py를 실행해도 동작합니다.
```powershell
python main.py
```

## 정답 실행 예
```text
Letterbox: (224, 224, 3) {'resized_wh': [224, 168], 'left': 0, 'top': 28, 'ratio': 0.7}
녹색 Mask 픽셀: 2091
```

## 실제 예상 결과
[expected/](expected/)의 CSV·JSON·PNG를 참고합니다. 영상은 첫 프레임 PNG와 수치 기록으로 확인합니다. 전체 AVI는 본인이 생성합니다.
PNG는 동일 입력/환경에서 픽셀 재현을 확인합니다. JPEG/MJPG는 손실 압축이며 파일 크기·시간·일부 경계는 빌드에 따라 달라질 수 있습니다.

## 완료 기준
224×224 안에 224×168 영상과 상하28픽셀 여백이 생깁니다. HSV 마스크에서 녹색 범위를 바꾸면 어떤 영역을 놓치는지 기록합니다.

## 설명 질문
처리 설정 한 가지를 바꾼다면 예상 결과는 무엇인가요? 실행 전에 예상을 적으세요.
어떤 정보가 사라졌고, 다음 모델의 입력으로 사용할 때 어떤 위험이 있나요?
