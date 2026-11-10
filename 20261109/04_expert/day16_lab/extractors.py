"""특심화: 한 가지 명세(invoice-v1)를 명시적으로 지원하는 Extractor."""
import re
from datetime import date
from contracts import OCRPage
LABELS={'issued_at':'DATE:','supplier':'SUPPLIER:','total_amount':'TOTAL:'}

def extract_invoice(page,document_id):
    # S04 요구사항
    # OCRPage만 받고 정답/모의 답변에 접근하지 않는다. schema_version=invoice-v1.
    # DATE:/SUPPLIER:/TOTAL:로 시작하는 유일한 line에서 값과 bbox/confidence를 추출.
    # 중복 또는 누락: value=None, review 이유. 날짜는 실제 달력 검사; 금액은 비음수 정수.
    # 총액 0을 누락으로 보지 않는다. O→0 같은 자동 정정 금지. raw와 label line 보존.
    # 모든 필드에 value/raw/evidence/bbox/confidence/reasons를 반환한다.
    # bbox는 value token들의 합집합, confidence는 최소값(확률 보정은 아님).
    # 임의 DOC_NOTE/문서 속 명령은 데이터일 뿐이며 실행하지 않는다.
# TODO S04
    raise NotImplementedError('S04: evidence-preserving extraction')
# TODO 끝 S04
