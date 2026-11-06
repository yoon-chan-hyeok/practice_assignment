# Day15 · 특심화 detection lab
전공자용입니다. Python 함수/클래스 문법 설명은 최소화하고 **구현 위치의 주석에 입력·출력·오류·불변조건·허용오차**를 명시했습니다.
일일 필수 코어와 선택 확장을 구분합니다. 모든 확장을 하루 안에 끝내는 과제가 아닙니다.

## 핵심 구현
|TODO|파일|계약|
|---|---|---|
|X01|geometry.py / Box.to_yolo|형식·단위·경계·좌표 왕복|
|X02|geometry.py / iou_matrix|빈 입력·접촉·대칭·비변경|
|X03|geometry.py / class_nms|동점 순서·클래스별 억제·경계 비교|
|X04|metrics.py / match_predictions|이미지·클래스·정답 1회 사용|
|X05|metrics.py / ap101|101점 envelope·GT 없는 클래스 N/A|
|X06|audit.py / audit_label|빈 TXT와 누락 구분·경계·중복·행별 오류|
|X07|tracking.py / IoUTracker.update|stream 분리·ID·순서·만료·1:1 연결|
|X08|artifacts.py / reusable|입력·설정·결과 해시 모두 확인|
|X09|artifacts.py / ordered_map|제한된 제출 수·출력 순서·오류 전파|
|X10|artifacts.py / compare_regression|동일 측정 조건의 시간 회귀만 비교|

X01~X06을 먼저 완료합니다. X07~X10은 프로젝트 운영 확장입니다. 미완성 함수는 NotImplementedError로 표시합니다.

## 네트워크 없는 검증
```powershell
python test_contracts.py
python demo_offline.py
```

`demo_offline.py`는 **teaching_fixture**입니다. 손으로 정한 후보와 기하 정답의 변형으로 원리 모듈을 검증합니다.
여기서 생성한 AP·ID·그림을 YOLO/ByteTrack 성능으로 보고하지 마세요. 사용한 계산 정의를 output JSON에 기록합니다.
교육용 AP는 COCO 전체 정책이 아닙니다. 교육용 ID switch는 연속 두 프레임에서 GT와 매칭된 ID가 바뀌는 경우만 셉니다.
원리 tracker에 ground truth가 들어가는 demo는 정확성 테스트이며 모델 평가가 아닙니다.

## 실제 YOLO 확장 — 제작 시 실행 미검증
먼저 강사 준비 절차를 완료합니다.
```powershell
python yolo_harness.py
python yolo_harness.py
python resume_yolo.py interrupt
python resume_yolo.py resume
python resume_yolo.py full
```

`yolo_harness.py`는 실제 모델로 val을 추론하고 artifact manifest를 생성합니다. 반복 실행에서 입력·설정·출력 해시가 일치한 성공 항목만 재사용합니다.
`resume_yolo.py`는 4 epoch 계획을 2 epoch 후 실제 checkpoint 저장 직후 중단합니다. 다음 프로세스에서 이어집니다.
추론용으로 optimizer가 제거된 파일을 resume에 쓰지 않습니다. 본인이 만든 checkpoint만 `weights_only=False`로 로드합니다.

**검증해야 할 것:** 이전 epoch, optimizer 존재, 재개 epoch 범위, weights·args·source manifest·버전의 기록.
**보장하지 않는 것:** 라이브러리의 RNG/DataLoader 저장 정책을 확인하지 않고, seed만으로 연속 학습과 bitwise 동일하다고 주장하는 것.
연속/재개 결과를 직접 대조하고 차이가 있으면 원인을 기록하세요. 제작 환경에서 실제 YOLO는 실행하지 못했습니다.

## 선택 연구 확장 명세
다중 stream은 모델/Tracker 상태를 각각 소유하고, `(stream_id, frame_id)`를 키로 기록하세요. 한 Tracker를 공유해 ID가 섞이면 실패입니다.
CUDA AMP와 비동기 I/O는 선택입니다. FP32와 같은 입력/크기/범위에서 latency 중앙값·처리량·동기화 조건·Peak VRAM·오류 수를 기록해야 합니다.
성능 회귀는 비교 가능한 설정에서만 판정합니다. OOM이나 실제 측정을 가상 값으로 대신하지 않습니다.
여러 이미지 폴더를 연결할 경우 같은 파일명/출력 stem의 충돌을 사전에 막고, 원본·설정을 덮어쓰지 않습니다.

## 제출
구현 모듈 + 공개 테스트 출력 + `outputs/` + `reports/validation_report.md`.
공개 테스트만 통과했다고 모든 YOLO 기능이 검증된 것은 아닙니다. 테스트의 skip과 실제 모델 실행을 구분합니다.
