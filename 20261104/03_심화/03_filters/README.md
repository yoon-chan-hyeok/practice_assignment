# 필터 모듈·시간

PPT 33장에 대응합니다. 구현 난이도는 기존 응용 수준입니다.

## 파일 역할
main.py에서 시작합니다. shared ../data는 원본이며 outputs/는 실행으로 생성됩니다. filters.py·video_ops.py가 있는 단원은 계산을 그 모듈에 둡니다.

## 구현할 부분
### H03 · `filters.py`
마지막 후보 bilateral을 d=7, sigmaColor=50, sigmaSpace=50으로 처리해 반환하세요. name은 정상 후보만 전달됩니다.

## 실행
현재 단원 폴더에서 다음을 실행합니다. 절대 경로로 main.py를 실행해도 동작합니다.
```powershell
python main.py
```

## 정답 실행 예
```text
필터/Edge 픽셀: [('gaussian', 3234), ('sharpen', 14866), ('bilateral', 8237)]
median_ms는 현재 CPU·OpenCV 환경의 7회 측정값입니다.
```

## 실제 예상 결과
[expected/](expected/)의 CSV·JSON·PNG를 참고합니다. 영상은 첫 프레임 PNG와 수치 기록으로 확인합니다. 전체 AVI는 본인이 생성합니다.
PNG는 동일 입력/환경에서 픽셀 재현을 확인합니다. JPEG/MJPG는 손실 압축이며 파일 크기·시간·일부 경계는 빌드에 따라 달라질 수 있습니다.

## 완료 기준
같은 입력·Canny 설정을 유지합니다. Edge 수는 참조 품질이 아니며, sharpen이 잡음 경계도 강화할 수 있습니다.

## 설명 질문
처리 설정 한 가지를 바꾼다면 예상 결과는 무엇인가요? 실행 전에 예상을 적으세요.
어떤 정보가 사라졌고, 다음 모델의 입력으로 사용할 때 어떤 위험이 있나요?
