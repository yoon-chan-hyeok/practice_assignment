"""원문과 근거를 보존하는 최소 문서 추출 모듈. 문서번호는 파일 ID로 관리합니다."""
import re
from datetime import date

PATTERNS = {'issued_at': r'^DATE:\s*(\d{4}-\d{2}-\d{2})\s*$', 'supplier':r'^SUPPLIER:\s*(.+)$', 'total_amount':r'^TOTAL:\s*(\d+)\s*$'}
LABELS = {'issued_at':'DATE:', 'supplier':'SUPPLIER:', 'total_amount':'TOTAL:'}

def extract(text, tokens=()):
    """3개 필드를 추출합니다. 정답 파일·VLM 응답을 참조하지 않습니다."""
    fields = {}
    for name, pattern in PATTERNS.items():
        matches = list(re.finditer(pattern, text, re.MULTILINE))
        value, raw, bbox, confidence = None, None, None, None
        warnings = []
        # 중복 라벨도 사람이 확인할 대상으로 남깁니다. 임의의 마지막 값을 선택하지 않습니다.
        if len(matches) != 1:
            warnings.append('missing_or_ambiguous')
        else:
            raw = matches[0].group(1).strip()
# TODO C07
            value = None
# TODO 끝 C07
            if name == 'issued_at':
                try:
                    date.fromisoformat(value)
                except (TypeError, ValueError):
                    value = None
                    warnings.append('invalid_date')
            anchors = [t for t in tokens if t['text'] == LABELS[name]]
            if len(anchors) == 1:
                a = anchors[0]
                same = [t for t in tokens if (t['page'],t['block'],t['paragraph'],t['line']) == (a['page'],a['block'],a['paragraph'],a['line']) and t['bbox'][0] >= a['bbox'][2]]
                if same:
                    bbox = [min(t['bbox'][0] for t in same),min(t['bbox'][1] for t in same),max(t['bbox'][2] for t in same),max(t['bbox'][3] for t in same)]
                    confidence = min(t['conf'] for t in same)
        fields[name] = {'raw':raw, 'value':value, 'bbox':bbox, 'confidence':confidence, 'warnings':warnings}
    return fields

def extract_items(text):
    """고정된 4열 서식만 처리합니다. 일반적인 표 구조 인식 모델은 아닙니다."""
    rows = []
    for line in text.splitlines():
        m = re.fullmatch(r'([A-Z]+) (\d+) (\d+) (\d+)', line.strip())
        if m:
            item,qty,price,amount = m.groups()
            rows.append({'item':item,'qty':int(qty),'unit_price':int(price),'amount':int(amount)})
    return rows

def validate(fields, items):
    """누락과 합계 관계를 점검합니다. 합계 0은 유효하며 누락(None)과 다릅니다."""
    reasons = [name+':missing' for name,f in fields.items() if f['value'] is None]
    for row in items:
        if row['qty'] * row['unit_price'] != row['amount']:
            reasons.append('row_arithmetic')
# TODO C08
    pass
# TODO 끝 C08
    return reasons

def reconcile(fields, responses):
    """OCR과 모의/실제 답변을 비교합니다. 일치도 원문 OCR의 진실성을 보장하지는 않습니다."""
    results = {}
    by_field = {r['field']:r for r in responses}
    for field, info in fields.items():
        response = by_field.get(field, {'answer':None,'evidence':''})
        label = LABELS[field]
        expected_evidence = label+' '+str(info['raw']) if info['raw'] is not None else ''
        # 단순 부분 문자열보다 라벨-값을 묶어 비교합니다.
# TODO C09
        supported = False
# TODO 끝 C09
        results[field] = {**info, 'vlm_answer':response['answer'], 'evidence':response['evidence'], 'evidence_supported_by_ocr':supported, 'review':not supported or bool(info['warnings']), 'final_value': info['value'] if supported else None}
    return results
