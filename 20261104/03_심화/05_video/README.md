# Frame 함수·보고서

PPT 53장에 대응합니다. 구현 난이도는 기존 응용 수준입니다.

## 파일 역할
main.py에서 시작합니다. shared ../data는 원본이며 outputs/는 실행으로 생성됩니다. filters.py·video_ops.py가 있는 단원은 계산을 그 모듈에 둡니다.

## 구현할 부분
### H05 · `video_ops.py`
Resize160×120→Gray→Gaussian3×3→Canny80/160 순서로 edge를 만드세요. 파일 열기·종료는 main이 담당합니다.

## 실행
현재 단원 폴더에서 다음을 실행합니다. 절대 경로로 main.py를 실행해도 동작합니다.
```powershell
python main.py
```

## 정답 실행 예
```text
Frame/FPS/크기: 48 12.0 (160, 120)
wall은 read·처리·write 포함, mean_process는 Frame 처리만 포함합니다.
```

## 실제 예상 결과
[expected/](expected/)의 CSV·JSON·PNG를 참고합니다. 영상은 첫 프레임 PNG와 수치 기록으로 확인합니다. 전체 AVI는 본인이 생성합니다.
PNG는 동일 입력/환경에서 픽셀 재현을 확인합니다. JPEG/MJPG는 손실 압축이며 파일 크기·시간·일부 경계는 빌드에 따라 달라질 수 있습니다.

## 완료 기준
48frame·12FPS·160×120으로 저장합니다. wall_s와 mean_process_ms의 측정 범위가 다름을 설명합니다.

## 설명 질문
처리 설정 한 가지를 바꾼다면 예상 결과는 무엇인가요? 실행 전에 예상을 적으세요.
어떤 정보가 사라졌고, 다음 모델의 입력으로 사용할 때 어떤 위험이 있나요?
