# Jetson·DeepStream 계획

PPT 73쪽 / 입출력 범위·워밍업·반복 측정·환경 기록을 설계합니다.

열 파일: `experiment.py`

**C06:** 지연시간 분포·처리량·메모리·온도·전력·드롭 수를 측정 계획에 넣으세요. 실행하지 않은 수치는 None으로 둡니다.

```powershell
python experiment.py
```

DeepStream 표기는 개념 흐름입니다. 실제 GStreamer caps·Pad 연결·Parser·Plugin은 장치에서 구성해야 합니다.

실제 실행 출력:

```text
decode -> nvstreammux -> nvinfer -> optional nvtracker -> nvdsosd -> sink
측정 항목: 7 하드웨어 실행: 미수행
```

결과: outputs/deployment_plan.json. 예상 결과는 `expected/`를 확인합니다.

완료 질문: Jetson의 공유 메모리와 dGPU VRAM을 숫자만으로 비교하면 왜 부정확할까요?

내 설명: ______________________________
