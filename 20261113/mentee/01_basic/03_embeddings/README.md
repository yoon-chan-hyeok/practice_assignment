# 실습 03 · Embedding·Cosine·시각화 · 기본필수

**PPT 기준:** 36장. 3단계 중 한 수준을 선택하며, 기본필수도 공통 목표를 충족할 수 있습니다.

**실습 목표:** 출력: cosine_report.json / vectors.png. 이 파일은 수업의 독립 시작점입니다. 앞 교시를 완료하지 못했더라도 이 폴더에서 진행할 수 있습니다.

## 실행

VS Code에서 이 수준의 폴더(`01_basic`)를 열고, 프로젝트 최상단에서 다음 명령을 실행하세요.

```powershell
python 03_embeddings/main.py
```

활성화 정책으로 가상환경 실행이 막힌다면, 프로젝트의 Python 실행 파일을 명시해서 실행하세요. 예: `.venv\Scripts\python.exe 03_embeddings/main.py`.

## TODO 목록 (3개)

1. **D20-03-B01** — A-B와 A-C 벡터의 Cosine Similarity를 계산하세요.
2. **D20-03-B02** — 점수의 부호·범위를 보고 어느 벡터 방향이 유사한지 판별하세요.
3. **D20-03-B03** — 2D 점 그래프와 cosine_report.json을 outputs에 저장하세요.

## 예상 결과 / 확인 기준

Cosine(A,B) ≈ 0.9701, Cosine(A,C) = -1.0. 기본 행렬 shape=(3,2), 응용·심화=(4,2).

유사도 계산 결과의 해석과 실제 모델 임베딩 품질을 구분

**출력 파일:** 실행 시 이 폴더의 `outputs/` 아래에 생성됩니다. 완성 전 `NotImplementedError`가 발생하는 것은 TODO 안내 동작입니다. 예상 결과가 달라지면 원본 데이터를 수정했는지·선택한 모델/시드가 같은지 먼저 확인하세요.

**주의:** 본 실습의 교육용 Tokenizer/Embedding/Logit은 실제 대규모 언어모델의 계산을 단순화한 것입니다. Transformer Tokenizer 및 SentenceTransformer 실제 호출은 루트의 `optional_examples`에서 별도로 안내하며 기본필수 요구사항이 아닙니다.
