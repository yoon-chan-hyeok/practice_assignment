# Day16 · OCR·VLM 미니 애플리케이션

## 역할과 작성 위치
`main.py`: 읽기·전처리·실행·저장. `fields.py`: 필드·표·검토 규칙. `evaluate.py`: 정답을 사용하는 평가 전용. `ocr_backend.py`: 선택 실제 OCR. `vlm_real.py`: 선택 로컬 실제 VLM.

TODO C07~C10을 완성합니다. C07은 자료형 정규화, C08은 합계, C09는 값·근거 대조, C10은 최종 저장입니다. 제공 함수를 복잡하게 늘리지 않습니다.

## 실행
```powershell
python main.py
# 선택: 같은 문서 5장을 실제 OCR하는 경로
python main.py --ocr live
```
기록 재생은 original PNG에 실행한 OCR입니다. 새로 저장한 binary.png의 추론 결과가 아닙니다. --ocr live 또한 원본 5장을 일괄 추론합니다. 전처리 결과 비교는 실습01의 명시된 별도 기록으로 합니다.

생성 파일: `outputs/final_documents.json`, `field_evaluation.csv`, `run_status.json`, 전처리·단어 Box·필드 근거 crop PNG 25개.

실습08은 설정을 바꾸지 않고 main.py를 다시 실행합니다. 출력 JSON과 CSV의 문서 수·필드 값·review 상태를 대조합니다. live OCR의 시간은 변동하며 비교 범위를 기록합니다.

## 출처와 보류
VLM은 기본적으로 mock입니다. doc04의 합계 불일치와 doc05의 근거 누락은 final_value=None과 검토 대상으로 남깁니다. OCR 기록 자체가 틀릴 가능성도 있으므로 일치만으로 사실성을 보장하지 않습니다. 정답은 `field_evaluation.csv` 생성 시점에만 사용합니다.

## 실제 VLM 선택
`python vlm_real.py --model-dir 로컬모델폴더 --image ../data/doc01.png --output local_vlm.json`으로 실제 모델 연결을 별도 시도합니다. 배포한 파일은 네트워크 다운로드를 자동 실행하지 않습니다. 제작 환경에서 실제 모델은 미검증이며 실패를 mock으로 대체하지 않습니다.

## 제출
완성 코드·결과 파일·`reports/model_review.md`를 제출합니다. 결과 수치보다 분모·근거·검토 이유·mock/real·측정 범위 설명이 중요합니다. 명세상 본 프로그램은 특정 4열 영문 서식만 지원합니다. 범용 문서 이해 제품이 아닙니다.
