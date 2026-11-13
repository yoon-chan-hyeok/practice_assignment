"""08개 main.py 실행 후 'python -m pytest tests -q'로 수행하는 심화 검증.

정답 구현 여부를 직접 검사하지 않고, 실행 결과의 주요 불변조건을 점검합니다.
"""
from pathlib import Path
import json
import math

ROOT=Path(__file__).resolve().parents[1]

def obj(folder,name):
    path=ROOT/folder/'outputs'/name
    assert path.exists(),f"먼저 {folder}/main.py를 실행하세요: {path}"
    return json.loads(path.read_text(encoding='utf-8'))

def test_token_budget():
    d=obj('02_tokenization','token_report.json')
    assert [r['count'] for r in d['records']]==[8,7,9]
    assert d['budget']['remaining']==500

def test_embeddings():
    d=obj('03_embeddings','cosine_report.json')
    assert math.isclose(d['cosine']['AB'],0.9701425,abs_tol=1e-4)
    assert math.isclose(d['cosine']['AC'],-1,abs_tol=1e-6)

def test_transformer_shape():
    d=obj('04_transformer','transformer_report.json')
    assert d['embedding']==[2,5,8] and d['encoder_output']==[2,5,8]

def test_attention():
    d=obj('05_attention','attention_report.json')
    for i,row in enumerate(d['weights']):
        assert abs(sum(row)-1)<1e-5
        assert all(row[j]==0 for j in range(i+1,len(row)))

def test_inference():
    d=obj('06_inference','inference_report.json')
    assert abs(sum(d['probs'])-1)<1e-5
    assert d['greedy']['index']==0

def test_daily_project():
    d=obj('08_daily_project','daily_project.json')
    assert d['scores_shape']==[3,3] and len(d['source_data'])==3
    assert all(abs(n-1)<1e-5 for n in d['row_sums'])
