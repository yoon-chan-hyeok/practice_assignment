# 특심화 · day13_lab

전공자 선택 경로입니다. **기능 이름보다 요구사항과 검증 조건을 먼저 읽습니다.** 함수·클래스 문법은 상세 반복 설명하지 않습니다.
실제 문제의 입력·출력·금지 동작·보존 상태·실패 조건은 각 TODO 바로 위 주석에 있습니다.
전체10곳이며 8교시 안에 모든 연구성 확장을 완료할 필요는 없습니다. 우선 핵심6곳(X01·X02·X03·X06·X09·X10)으로 이미지 프로젝트를 완성하고, 나머지4곳은 품질·영상 확장입니다.

## 파일 역할과 PPT 대응
| PPT 실습 | 구현할 파일 | TODO | 요구 결과 |
|---|---|---|---|
| 01 | contracts.py | X01 | BGR 계약·메모리독립·기준 패치 검사 |
| 02 | geometry.py | X02·X03 | Letterbox와 좌표 왕복 <=1e-9 |
| 03 | quality.py | X04 | MSE·시간 Pareto 후보. 동점 보존 |
| 04 | quality.py | X05 | IoU·연결요소·원본 보존 |
| 05 | video_pipeline.py | X07·X08 | bounded 큐·드롭 회계·리소스 종료 |
| 06 | augmentation.py | X06 | 표본ID/seed 기반·worker 순서 무관 증강 |
| 07~08 | cache.py | X09·X10 | Config key·실패 기록·손상 출력 재처리 |

engine.py·main.py·run_experiments.py는 실행 골격입니다. 구현해야 할 알고리즘을 대신 완성한 파일은 아닙니다.
`test_public.py`는 공개 계약 검사이며 보고서 해석을 대신 채점하지 않습니다. 미완성 코드는 NotImplementedError가 정상적인 표시입니다.

## 입력
정상 파일은 data/에 있습니다. manifest의 train4장·valid1장·test1장은 설명용 분할입니다. 학습 모델을 만들지 않습니다.
무작위 증강은 train에만 적용하며 valid/test의 augment 함수는 원본 copy를 반환합니다. 이후 고정 Resize·Edge는 세 split 모두 동일 계약으로 적용합니다.
Mask truth는 합성 도형을 만들 때 함께 만든 정답이며 품질 지표가 성립하는 근거입니다.
코덱 실패·손상 PNG 같은 실패 사례는 tests가 임시 폴더에서만 만듭니다. 원본 data는 훼손하지 않습니다.

## 실행 순서
이 README가 있는 day13_lab 폴더에서 실행합니다. subprocess/Worker는 Windows 호환을 위해 spawn과 main guard를 사용합니다.

```powershell
python run_experiments.py --task geometry
python main.py --workers 1
python main.py --workers 2 --output outputs/parallel
python main.py --workers 2 --output outputs/parallel --resume
python compare_runs.py
python test_public.py
```

첫 단독 실행은 total6·ok6·failed0·reused0, 이어진 resume는 reused6을 기대합니다. Worker1/2의 PNG hash와 변환 설정이 일치해야 합니다.
`--resume`는 실패 항목·원본 변경·config 변경·출력 손상을 감지하면 해당 항목을 다시 처리합니다. 단순한 파일 존재 체크로 건너뛰지 않습니다.
`events.jsonl`에는 각 실행의 모든 항목을 추가 기록합니다. `cache.json`은 최신 상태입니다. 실패가 있으면 main의 종료코드는1입니다.
config.json은 size·seed·blur·canny만 받습니다. Worker 수·출력 위치는 처리 의미가 아니므로 key에서 제외합니다.

확장 실험:
```powershell
python run_experiments.py --task quality
python run_experiments.py --task augment
python run_experiments.py --task video
```

## 핵심 계약
**색 순서:** 임의 자연 영상만으로 RGB/BGR를 확정할 수 없습니다. X01은 알려진 기준 패치가 제공된 경우만 색 기준을 검사합니다.
**좌표:** 경계좌표 [0,W]×[0,H]의 xyxy를 사용합니다. 반올림 뒤 실제 가로·세로 배율을 따로 기록합니다. 픽셀 중심 보간과 혼동하지 않습니다.
**재현성:** Python hash나 Worker번호 대신 SHA256(seed,ID,variant)로 로컬 RNG를 만듭니다. 같은 런타임에서 Worker1/2가 동일해야 합니다. 미래 버전 전체의 bitwise 동일성을 보장하지 않습니다.
**라벨:** 기하 도형 존재의 의미를 유지하는 변환만 허용합니다. 문자/방향 클래스라면 allow_flip/allow_rotate를 False로 지정하고 정책을 다시 설계합니다.
**품질:** MSE·IoU는 동일 기준영상/합성 truth에 대해서만 계산합니다. Edge 수나 객체 개수만으로 최고 품질을 정하지 않습니다.

## 영상 큐 실험의 의미
block은 모든 Frame을 순서대로 저장합니다. drop_latest는 입력 큐가 가득 찼을 때 새 Frame을 버립니다.
종료 sentinel은 드롭하지 않습니다. 처리·encode 오류는 cancel로 전파하고 cap/writer를 release한 뒤 실패를 반환합니다.
정상 종료 시 decoded = written + dropped, index는 단조 증가·중복 없음, 큐 길이는 capacity 이하입니다.
queue_peak는 qsize를 샘플링한 값이며 정밀한 최대 점유량 추적기가 아닙니다.
latency는 decode 완료부터 writer.write 반환까지이며 카메라 센서부터 파일 저장장치까지의 실시간 지연이 아닙니다.
드롭 시 원본 FPS를 유지한 CFR 영상이므로 재생시간이 짧아집니다. 원본 PTS나 원래 시간 간격 보존을 주장하지 않습니다. frame_map.csv로 원본 index/time을 남깁니다.
처리 지연3ms는 드롭 동작을 관찰하는 모의 조건입니다. 드롭 수·시간·Pareto 후보는 실행마다 달라도 됩니다. 멀티스레드가 항상 빠르다고 주장하지 않습니다.

## 재현 결과와 검증
expected/는 정답을 실제 실행한 기록입니다. 표·설정·영상 회계를 비교하고 시간의 정확한 숫자는 정답으로 삼지 않습니다.
공개 테스트는 정상·경계·계약 실패·Worker재현·재개·영상회계·오류 전파를 확인합니다. FFV1 코덱 미지원 환경은 해당 테스트만 skip입니다.
테스트에서 사용한 API는 CPU입니다. GPU/CUDA 성능 검증을 했다고 표시하지 마세요.

## 제출
완성한 코드와 config, outputs의 summary/cache/events·기하/품질/증강/영상 기록, reports/engineering_report.md를 제출합니다.
비결정적인 시간·드롭 수와 결정적인 픽셀/설정 결과를 분리하고, 환경·코덱·측정 범위·실패 복구 증거를 남깁니다.
입력 hash와 config key는 보안 서명·변조 불가 장치가 아닙니다. 실험 재개 판단용입니다.
