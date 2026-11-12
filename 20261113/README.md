# 2026-11-13 Day20 · LLM·Transformer 실습 (수강생/강사 통합)

**기준 PPT:** `Day20_LLM_Transformer_20261113_QUALITY.pptx` (총 90장)
**목표:** 11/10~12에 완성한 지식 관리 API·DB 위에서, LLM 입력→계산→다음 Token 원리를 설명할 수 있다.

이 자료는 11/13의 **학습 원리 실습**이며 실제 LLM API·RAG 파이프라인·Agent 동작을 새로 완성하지 않습니다. 11/16 Prompt, 11/18 Embedding/Vector DB, 11/20 RAG 과정을 위한 기반입니다.

## 난이도 · 배포

| 수준 | 폴더명 | 구현 TODO | 주요 범위 |
|---|---|---:|---|
| 기본필수 | `01_basic` | 30 | 가장 작은 코드에서 핵심 결과 계산·설명 |
| 응용 | `02_intermediate` | 46 | 비교 조건·그래프·진입점/계산 분리 |
| 심화 | `03_advanced` | 63 | 수치 검증·Head/Mask·학습 단계·역할별 구조 |

- `mentee/`: 미완성 코드와 TODO 주석·예상 결과·실행 안내. **학생 배포용**입니다.
- `mentor/`: 동일한 파일 위치의 모든 TODO를 완성하고 핵심 계산 주석·검수 자료를 포함합니다. **정답이 있으므로 수강생 배포 금지**입니다.
- 세 수준은 각각 독립적인 학습 경로입니다. 기본필수만으로 공통 평가 100점이 가능합니다.
- 01~07 중 하나가 미완성이더라도 **다음 교시의 독립된 제공 코드**로 이어갈 수 있습니다.
- 08은 마지막 일일프로젝트이며 01~07의 개념 계산을 한 프로젝트에서 종합합니다.

## 설치 및 실행 (Windows 11·VS Code)

```powershell
# 압축을 푼 최상위 폴더에서 실행
py -m venv .venv
.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt

# mentee의 기본필수 2교시 예시
.\\.venv\\Scripts\\python.exe mentee/01_basic/02_tokenization/main.py
```

Windows PowerShell에서 가상환경 활성화를 막는 경우, 위처럼 가상환경의 Python 파일 경로를 직접 사용하면 됩니다. 가상환경이 이미 준비된 경우 재사용해도 됩니다.

## 완료 결과

- 01: `architecture.md/.json` (API/DB/LLM/응답 역할과 연결)
- 02: `token_report.json` (A/B/C 토큰·ID·Mask·Context 예산)
- 03: `vectors.png`, `cosine_report.json` (A-B ≈ 0.9701, A-C = -1)
- 04: `transformer_report.json` (2×5 → 2×5×8 → 2×5×8)
- 05: `attention_report.json` (+ 응용/심화는 Heatmap, 행합=1·마스크 위치=0)
- 06: `inference_report.json` (Logit→Softmax·Temperature)
- 07: `review.json/.md` (사실·형식·근거 문제 구분)
- 08: `daily_project.json`, `one_page_summary.md` (일일프로젝트 공통 결과)

## 모델 다운로드가 없어도 가능한 이유

기본 실습에는 로컬에서 재현되는 **학습용 ToyTokenizer와 작은 벡터, PyTorch 계산**을 사용합니다. 이는 실제 다국어 BERT Tokenizer/사전학습 SentenceTransformer의 결과와 다릅니다. 학습용 유사도 값·Attention 분포를 실제 자연어 모델의 의미 성능이나 답변 근거로 해석하지 않습니다.

선택 시연: `optional_examples/real_hf_tokenizer.py`, `optional_examples/real_sentence_embedding.py`는 설치 및 로컬 캐시가 있을 때만 수행합니다. **기본 실행 시 네트워크를 사용하지 않으며**, 명시적으로 `--allow-download`를 사용한 경우에만 모델 다운로드를 허용합니다.

## 제출과 평가

별도의 장문 보고서는 필요하지 않습니다. 본인의 수준에서 생성한 `outputs/` 결과와 마지막 `one_page_summary.md`로 설명합니다. PPT 83장의 공통 평가: **Token·Context 25 / Embedding 20 / Attention 25 / 학습·추론 15 / 플랫폼 연결 15**입니다.

**주의:** 이 실습에 실제 개인정보, API 키, 회사 내부 비밀을 포함하지 않습니다.
