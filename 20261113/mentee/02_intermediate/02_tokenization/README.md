# 실습 02 · Token·ID·Context 분석 · 응용

**PPT 기준:** 26장. 3단계 중 한 수준을 선택하며, 기본필수도 공통 목표를 충족할 수 있습니다.

**실습 목표:** 출력: token_report.json. 이 파일은 수업의 독립 시작점입니다. 앞 교시를 완료하지 못했더라도 이 폴더에서 진행할 수 있습니다.

## 실행

VS Code에서 이 수준의 폴더(`02_intermediate`)를 열고, 프로젝트 최상단에서 다음 명령을 실행하세요.

```powershell
python 02_tokenization/main.py
```

활성화 정책으로 가상환경 실행이 막힌다면, 프로젝트의 Python 실행 파일을 명시해서 실행하세요. 예: `.venv\Scripts\python.exe 02_tokenization/main.py`.

## TODO 목록 (6개)

1. **D20-02-I01** — 제공된 지식 A/B/C 세 문장을 학습용 Token·Token ID로 변환하세요.
2. **D20-02-I02** — 길이가 다른 두 입력을 Padding하고 attention_mask의 0/1을 확인하세요.
3. **D20-02-I03** — PPT 문맥 예시(300+1200+2000+150, 출력 예약 850)의 합과 남는 예산을 계산하세요.
4. **D20-02-I04** — max_length=5와 12의 Truncation 여부·실제 길이를 비교하세요.
5. **D20-02-I05** — 실제 Token 수와 패딩 포함 Tensor 길이를 나누어 기록하세요.
6. **D20-02-I06** — Token·Mask·문맥 예산 결과를 outputs/token_report.json에 저장하세요.

## 예상 결과 / 확인 기준

교육용 Token 수(A,B,C) = (8,7,9), BOS/EOS 포함. PPT 예시 입력 3,650 + 출력 예약 850 = 4,500, Window 5,000에서 500 남음.

패딩 길이와 실제 Token 수를 혼동하지 않으며 Mask=0인 위치가 PAD

**출력 파일:** 실행 시 이 폴더의 `outputs/` 아래에 생성됩니다. 완성 전 `NotImplementedError`가 발생하는 것은 TODO 안내 동작입니다. 예상 결과가 달라지면 원본 데이터를 수정했는지·선택한 모델/시드가 같은지 먼저 확인하세요.

**주의:** 본 실습의 교육용 Tokenizer/Embedding/Logit은 실제 대규모 언어모델의 계산을 단순화한 것입니다. Transformer Tokenizer 및 SentenceTransformer 실제 호출은 루트의 `optional_examples`에서 별도로 안내하며 기본필수 요구사항이 아닙니다.
