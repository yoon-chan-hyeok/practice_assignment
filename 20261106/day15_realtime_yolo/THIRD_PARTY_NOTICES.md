# 자료 출처 및 외부 의존성

- 프로젝트의 실습 안내, 보고서 양식, 실행/점검 스크립트는 이번 요청에 맞게 작성했습니다.
- `assets/day15_demo.avi`는 사용자가 제공한 `day15_detection.zip`의 `data/demo.avi`를 그대로 복사한 파일입니다. 합성 도형 영상이며 실제 일상 물체 탐지 정확도 평가 자료가 아닙니다.
- Ultralytics/PyTorch/OpenCV/NumPy/PyYAML/Pillow 등 외부 Python 라이브러리는 이 ZIP에 포함하지 않았습니다. 설치는 별도입니다.
- YOLO26 가중치도 포함하지 않았으며, 프로그램은 공식 모델 이름을 이용해 최초 다운로드하도록 작성했습니다. 모델 클래스와 출처는 공식 문서를 확인하세요.
- Ultralytics 이용·배포 조건: https://www.ultralytics.com/license
- 구현 근거가 된 공식 기술 문서 목록은 README 하단에 있습니다.
- Python 소스에 API 호출 예시가 있지만 실제 카메라/YOLO 학습 실행까지 제작 환경에서 검증한 것은 아닙니다. `docs/TESTING.md`를 참고하세요.
