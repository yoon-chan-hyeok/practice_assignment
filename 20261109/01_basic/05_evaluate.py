"""실습 05: 5문서×3필드의 일치율을 구합니다. 정답은 평가할 때만 읽습니다."""
from pathlib import Path
import json
import re
import pandas as pd

base = Path(__file__).resolve().parent
lesson = json.loads((base / 'lesson.json').read_text(encoding='utf-8'))
rows = []
for name, doc in lesson['documents'].items():
    text = doc['ocr']['text']
    predicted = {'issued_at': re.search(r'DATE: (\d{4}-\d{2}-\d{2})', text).group(1), 'supplier': re.search(r'SUPPLIER: (.+)', text).group(1), 'total_amount': int(re.search(r'TOTAL: (\d+)', text).group(1))}
    for field in ['issued_at', 'supplier', 'total_amount']:
        # ========================================================
        # TODO B06: OCR 추출 결과와 실제 정답 비교
        # ========================================================
        #
        # [요구사항]
        # 1. 현재 문서(doc)에서 해당 필드(field)의 실제 정답을 가져오세요.
        #    - issued_at    : 문서 발행 날짜
        #    - supplier     : 공급업체 이름
        #    - total_amount : 총금액
        #
        # 2. OCR에서 추출한 예측값(predicted[field])과
        #    실제 정답값을 비교하세요.
        #
        # 3. 두 값이 정확히 일치하면 correct = True,
        #    일치하지 않으면 correct = False로 설정하세요.
        #
        # 4. 문자열은 문자열끼리, 숫자는 숫자끼리 비교하세요.
        #    - 날짜: "2026-11-09" == "2026-11-09" → True
        #    - 업체: "ABC" == "XYZ" → False
        #    - 금액: 150000 == 150000 → True
        #
        # [주의사항]
        # - 정답은 모델의 예측값을 생성할 때 사용하지 않습니다.
        # - 평가 단계에서만 정답을 읽어 비교합니다.
        # - correct 변수에는 반드시 True 또는 False를 저장합니다.
        # - 실제 정답의 저장 위치는 lesson.json 구조를 확인하세요.
        #
        # [기대 결과]
        # 문서 5개 × 필드 3개 = 총 15개의 일치 여부를 평가합니다.
        # ========================================================
        correct = False
        # TODO 끝 B06
        rows.append({'document_id': name, 'field': field, 'predicted': predicted[field], 'correct': correct})
table = pd.DataFrame(rows)
table.to_csv(base / 'p05_field_scores.csv', index=False, encoding='utf-8-sig')
print('문서 수:', len(lesson['documents']), '필드 수:', len(table))
print('필드 일치:', int(table['correct'].sum()), '/', len(table))
print('합성 영어 문서의 기록 비교이며 일반 OCR·한국어 성능이 아닙니다.')
