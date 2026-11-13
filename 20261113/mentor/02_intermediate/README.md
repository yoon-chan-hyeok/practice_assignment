# 2026-11-13 Day20 · 응용 (02_intermediate)

**총 TODO 46개**, 8개 교시 실습입니다. 하나의 난이도를 선택하면 됩니다. 기본필수부터 세 난이도를 모두 순서대로 수행해야 하는 구조가 아닙니다.

파일 구조는 **실습 성격에 맞는 main.py + analysis.py 책임 분리**로 구성했습니다. 폴더를 많이 만드는 것 자체는 학습 목표가 아닙니다.

## 시작 순서

1. 각 교시의 `README.md`와 PPT 안내 슬라이드를 읽습니다.
2. 그 폴더의 `main.py`를 실행합니다. 미완성 코드에서는 `NotImplementedError`가 정상적으로 발생할 수 있습니다.
3. `# TODO D20-...`와 `# BEGIN` / `# END` 사이를 완성합니다. (분리된 경우 `analysis.py`에 TODO가 있습니다.)
4. `outputs`에 생성된 JSON/그림/Markdown을 `expected/expected_results.md`와 대조합니다.
5. 마지막 08은 이전 단계의 학습 예제를 통합하지만, 이전 폴더 출력물에 의존하지 않습니다.

## 교시별 실행 명령 (VS Code 터미널·PowerShell)

- 1교시 · AI 서비스 구성요소 연결 (PPT 15장, TODO 1개): `python 01_ecosystem/main.py`
- 2교시 · Token·ID·Context 분석 (PPT 26장, TODO 1개): `python 02_tokenization/main.py`
- 3교시 · Embedding·Cosine·시각화 (PPT 36장, TODO 1개): `python 03_embeddings/main.py`
- 4교시 · Transformer 구조·Shape (PPT 47장, TODO 1개): `python 04_transformer/main.py`
- 5교시 · Self-Attention·Mask·Heatmap (PPT 58장, TODO 1개): `python 05_attention/main.py`
- 6교시 · 학습·추론·Sampling (PPT 68장, TODO 1개): `python 06_inference/main.py`
- 7교시 · LLM 한계·검증·RAG/Agent (PPT 76장, TODO 1개): `python 07_limits/main.py`
- 8교시 · 문장 하나가 LLM 출력이 되기까지 (PPT 82장, TODO 1개): `python 08_daily_project/main.py`


## 오프라인 동작 원칙

- 기본 실습에 필요한 외부 모델 다운로드는 없습니다. `torch`, `numpy`, `matplotlib`는 사전에 준비합니다.
- 제공된 `common/support.py`의 토큰화는 **교육용 regex/고정 어휘표**이고, 실제 BERT 토크나이저와 다릅니다.
- 교육용 2D 벡터는 사전학습된 의미 임베딩이 아닙니다. Attention도 자연어 모델의 학습된 주의 분포가 아닙니다.
- 실제 모델 시연은 `optional_examples/`를 별도로 사용하며 설치/다운로드 여부를 기록합니다.
- 결과를 받았다면 **값이 무엇을 의미하는지, Mask·Shape가 왜 필요한지** 스스로 설명합니다.

## 파일 경로

코드는 `Path(__file__)`를 사용하여 실행 폴더가 달라도 데이터를 읽고 결과를 해당 교시 `outputs/`에 저장합니다. 파일·폴더명은 영문과 숫자/밑줄로 통일하고, 한글은 문서·주석·샘플 문장에만 사용합니다.
