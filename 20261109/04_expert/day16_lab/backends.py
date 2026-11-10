"""실제 모델과 모의 응답의 출처를 반드시 분리합니다."""
import json
import copy
from pathlib import Path

class MockVLM:
    name='mock'
    def __init__(self,documents):self.documents=documents
    def ask(self,document_id,image_path):
        responses=copy.deepcopy(self.documents[document_id]['mock_vlm']['responses'])
        return {'backend':'mock','model_id':None,'latency_ms':None,'raw':json.dumps({'answers':responses},ensure_ascii=False)}


def make_backend(name,documents,model_dir=None):
    # S08 요구사항
    # 허용 name은 mock 또는 real. mock은 fixture의 mock_vlm만 읽어야 한다.
    # real은 model_dir이 실제 디렉터리인 경우에만 LocalVLM 생성(선택 설치 필요).
    # real import/모델 로딩 실패를 mock으로 바꿔 실행하면 안 된다.
    # 없는 폴더는 FileNotFoundError, 잘못된 backend는 ValueError.
    # mock 결과에 model id나 실제 추론시간을 조작해서 넣지 않는다.
# TODO S08
    raise NotImplementedError('S08: explicit backend selection')
# TODO 끝 S08
