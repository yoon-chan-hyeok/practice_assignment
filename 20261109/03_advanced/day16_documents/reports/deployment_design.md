# 배포 설계 (실제 실행 아님)

학습된 신경망 → ONNX 변환 및 수치 대조 → 대상 환경 TensorRT build → Runtime 수치·성능 확인.

TensorRT 10.x 예시:
```text
trtexec --onnx=model.onnx --saveEngine=model.plan --fp16
```
TensorRT 11.x 예시:
```text
python -m modelopt.onnx.autocast --onnx_path model.onnx --output_path model_fp16.onnx
trtexec --onnx=model_fp16.onnx --saveEngine=model.plan
```
위 ONNX 파일은 제공하지 않습니다. 실제 모델을 export하고 검증한 뒤 해당 설치 버전의 help로 명령을 다시 확인해야 합니다.

DeepStream 개념: source/decode → nvstreammux → nvinfer → optional nvtracker → nvdsosd → sink.
OCR·VLM의 입력 변환·출력 parser·tokenizer/문서 후처리는 모델별 통합이 별도로 필요합니다.

장치/JetPack/드라이버/CUDA/TensorRT/DeepStream: ___
입력 크기·dtype·정밀도·엔진 hash: ___
워밍업/반복수/측정범위: ___
결과 정확도와 허용오차: ___
p50/p95/FPS/온도/전력/메모리/드롭: 실제 장비가 없으면 모두 N/A
