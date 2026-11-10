"""특심화: JSON 유효성·근거·정답은 별개의 차원입니다."""
import json
import re
import math


def parse_vlm(raw):
    # S05 요구사항
    # 원문 JSON 한 개만 받는다. 코드펜스/주석/뒤따르는 문장을 자동 수리하지 않는다.
    # 최상위 keys 정확히 answers. answers에는 issued_at/supplier/total_amount가 각각 한번.
    # 항목 keys 정확히 field/answer/evidence. answer는 문자열/비음수 int/None 규칙 적용.
    # bool을 금액으로 허용하지 않는다. evidence는 문자열; null 답도 근거 정책은 후속 검사.
    # 중복 JSON 키도 거부해야 한다. 실패 시 ValueError. 임의 eval이나 exec 금지.
# TODO S05
    raise NotImplementedError('S05: strict VLM JSON')
# TODO 끝 S05


def decide(ocr_fields,answers,min_confidence=80.0):
    # S06 요구사항
    # OCR 추출과 VLM answer 자료형/값이 같고, evidence가 해당 OCR 라벨 줄과 정확히 같으며,
    # OCR confidence가 finite 임계값 이상이고 기존 reasons가 없을 때만 auto_accept.
    # 그 외는 final_value=None, status=review와 구체적 사유. 0은 유효한 값.
    # confidence None은 낮은 신뢰도; 없다고 100으로 채우지 않는다.
    # mock/real 출처는 호출자가 별도로 붙인다. 근거 일치도 픽셀 사실성의 보증이 아니다.
    # 입력 사전은 수정하지 않고 새 결과를 반환. gold/정답 인자는 없다.
# TODO S06
    raise NotImplementedError('S06: review policy')
# TODO 끝 S06


def redact_for_demo(text):
    """로그 예시의 이메일·전화만 마스킹합니다. 완전한 개인정보 탐지기가 아닙니다."""
    text=re.sub(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', '[EMAIL]',text)
    return re.sub(r'\b01[016789][- ]?\d{3,4}[- ]?\d{4}\b','[PHONE]',text)
