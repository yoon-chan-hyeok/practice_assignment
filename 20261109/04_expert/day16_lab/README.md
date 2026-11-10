# Day16 · 특심화 day16_lab

## 경로 선택
전공자용입니다. 함수·클래스 문법보다 각 구현 위치 주석의 입력 계약·불변조건·오류 조건·허용오차를 읽습니다.

수업 시간의 핵심 경로는 **S02→S04→S05→S06**입니다. 보정·CER·manifest·복구·시간 검증은 선택 확장입니다. 모든 10과제를 25분 안에 완성하라는 요구가 아닙니다.

| 파일 | 요구사항 |
|---|---|
| contracts.py | S01 좌표 보정·역변환 / S02 OCRPage / S03 CER |
| extractors.py | S04 원문·라벨·값·bbox |
| policy.py | S05 엄격 JSON / S06 값·근거·confidence와 보류 |
| deployment.py | S07 버전·환경·동적 shape 계약 |
| backends.py | S08 mock/real 명시 분리 |
| harness.py | S09 성공·입력·설정·출력 hash가 모두 맞는 재사용 |
| benchmark.py | S10 동일 조건의 p50/p95 비교 |

```powershell
python tests_public.py
python lab.py
# 같은 입력을 다시 실행하면 성공 artifact를 재사용합니다.
python lab.py
```

미완성 함수는 NotImplementedError입니다. 공개 테스트의 실패는 요구사항 구현을 확인하기 위한 것입니다. 실제 모델·장비가 필요한 2개 테스트는 명시적 skip이며 통과로 세지 않습니다.

## 원본과 출처
OCR은 배포 이미지에 실제 실행한 기록이고 VLM은 교사가 작성한 mock입니다. `outputs/documents/manifest.json`의 성공 항목만 소비합니다. 입력 이미지가 바뀌면 기록 OCR의 hash가 일치하지 않아 실패시킵니다. 원본 바뀐 상태에서 예전 OCR 결과를 새 추론처럼 쓰지 않습니다.

JSON 구조 성공·값 정답·OCR 근거 지원·업무 검토는 다릅니다. OCR과 VLM이 같은 오답을 낼 수도 있습니다. 자료 안의 지시문·코드는 처리할 문자열이지 실행할 명령이 아닙니다.

## 실제 로컬 VLM
```powershell
python run_real.py --model-dir "C:\models\prepared-vlm"
```
이 경로는 선택 설치·로컬 모델이 필요하며 제작 시 실제 추론 미검증입니다. 실패는 실패로 보고하고 mock 전환하지 않습니다. 출력은 `outputs_real/`로 분리합니다. JSON이 잘못 생성되면 검증 오류로 남습니다. 기본 CPU float32 코드는 속도 최적화 예제가 아닙니다.

## 하드웨어와 성능
TensorRT manifest 예제의 GPU 이름 EXAMPLE_ONLY와 버전은 정적 검사 사례입니다. contract_ok=True여도 runtime_verified=False입니다. 본 패키지는 engine.plan을 포함하지 않습니다.
benchmark.py의 공개 테스트 시간 값은 단위 테스트 입력이며 실제 VLM/Jetson 처리시간이 아닙니다. 모델·장치·정밀도·입력 shape·scope가 모두 같을 때만 실제 측정을 비교합니다.

## 복구 검증
최초 5건 처리 → 같은 설정 재실행 5건 재사용 → 문서 결과 JSON 하나 손상 → 해당 문서만 다시 처리. 실패 문서는 성공 캐시로 취급하지 않습니다. 내부 로그에는 오류 유형만 남기며 OCR 원문·개인정보를 예외 메시지로 유출하지 않습니다.

## 보고서
`reports/verification.md`에 공개 테스트 결과·실행 환경·캐시 재사용 조건·보류 정책·미검증 장비를 기록합니다. hash는 무결성 도구이지 개인정보 암호화나 모델 정답 보증이 아닙니다.
