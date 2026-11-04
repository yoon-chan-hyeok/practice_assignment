# 종합 프로젝트·실습07~08

PPT 71장에 대응합니다. 구현 난이도는 기존 응용 수준입니다.

## 파일 역할
main.py는 읽기·결과 저장, image_ops.py는 이미지 변환, video_ops.py는 프레임 반복, validate.py는 재읽기 확인입니다.
data/는 원본, expected/는 정답 예시, outputs/는 본인 실행 결과, reports/는 본인 설명입니다.

## 구현할 부분
### H07 · `image_ops.py`
Gray와 size=(너비,높이)로 축소한 small을 만드세요. 원본 image를 직접 수정하지 않습니다.

### H08 · `video_ops.py`
prepare_image(frame)의 edge 결과를 3채널로 바꾸고 writer에 전달하세요.

### H09 · `main.py`
results의 각 stage/result를 PNG로 저장하고 재읽기 비교와 크기·채널을 rows에 기록하세요. CSV 열은 코드의 예시 구조를 참고합니다.

### H10 · `validate.py`
읽은 image의 존재·(높이,너비)·dtype·채널을 CSV와 비교해 bool ok를 만드세요. 보고서의 의미 판단을 자동 채점하는 코드는 아닙니다.

## 실행
현재 단원 폴더에서 다음을 실행합니다. 절대 경로로 main.py를 실행해도 동작합니다.
```powershell
python main.py
python validate.py
```

## 정답 실행 예
```text
이미지 처리표: 21 행
영상 Frame/FPS: 48 12.0
다음: python validate.py
```

validate.py 결과:
```text
{'image_rows': 21, 'images_ok': True, 'source_unchanged': True, 'video_ok': True}
```

## 실제 예상 결과
[expected/](expected/)의 CSV·JSON·PNG를 참고합니다. 영상은 첫 프레임 PNG와 수치 기록으로 확인합니다. 전체 AVI는 본인이 생성합니다.
PNG는 동일 입력/환경에서 픽셀 재현을 확인합니다. JPEG/MJPG는 손실 압축이며 파일 크기·시간·일부 경계는 빌드에 따라 달라질 수 있습니다.

## 완료 기준
이미지3장×7단계의21행과 영상48frame, 원본 hash 유지·재읽기를 확인합니다. 영상/사진의 의미가 개선되었다는 평가는 사람이 확인합니다.

## 설명 질문
처리 설정 한 가지를 바꾼다면 예상 결과는 무엇인가요? 실행 전에 예상을 적으세요.
어떤 정보가 사라졌고, 다음 모델의 입력으로 사용할 때 어떤 위험이 있나요?
