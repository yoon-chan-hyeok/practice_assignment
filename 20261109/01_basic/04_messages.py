"""실습 04: 이미지+질문을 구성하고 모의 응답을 읽습니다. 실제 VLM을 호출하지 않습니다."""
from pathlib import Path
import json

base = Path(__file__).resolve().parent
lesson = json.loads((base / 'lesson.json').read_text(encoding='utf-8'))
doc = lesson['documents']['doc01']
rows = []
for answer in doc['mock_vlm']['responses']:
    question = lesson['questions'][answer['field']]
# TODO B05
    messages = []
# TODO 끝 B05
    rows.append({'backend': 'mock', 'messages': messages, 'response': answer, 'model_id': None, 'inference_ms': None})
    print(question, '->', answer['answer'])
(base / 'p04_mock_answers.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
print('MOCK: 교사가 작성한 응답 예시입니다. 실제 모델 출력이 아닙니다.')
