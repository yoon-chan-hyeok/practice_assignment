"""강의 공통 오프라인 계산 도구: 실제 사전학습 LLM이 아닙니다.

교육용 정규표현식 토큰화·작은 벡터·가중치 계산만 제공합니다.
Transformer의 tokenizer/embedding 품질을 이 도구로 평가할 수 없습니다.
"""
from pathlib import Path
import json
import math
import re
import torch

DATA = [
    {"id":"A", "title":"실습 파일 보관", "content":"실습 파일은 개인 폴더에 보관합니다.", "category":"learning"},
    {"id":"B", "title":"서버 실행", "content":"프로젝트 폴더에서 서버를 실행합니다.", "category":"environment"},
    {"id":"C", "title":"질문 작성", "content":"오류 메시지와 시도한 작업을 함께 적습니다.", "category":"learning"},
]
SPECIAL = ["[PAD]", "[UNK]", "[BOS]", "[EOS]"]

def words(text: str) -> list[str]:
    """교육용: 한글 연속 글자/영문/숫자/문장부호 분리. 서브워드 토크나이저가 아님."""
    return re.findall(r'[가-힣]+|[A-Za-z]+|\d+|[^\w\s]', text)

class ToyTokenizer:
    """BERT tokenizer 대체가 아닌, 오프라인 개념 확인용 규칙 기반 어휘표."""
    def __init__(self, corpus):
        wordset=sorted({word for line in corpus for word in words(line)})
        self.vocab={tok:i for i,tok in enumerate(SPECIAL + wordset)}
        self.reverse={i:t for t,i in self.vocab.items()}

    def encode(self, text: str, max_length=None, padding_to=None):
        raw=words(text)
        tokens=["[BOS]"]+raw+["[EOS]"]
        truncated=False
        if max_length is not None:
            if max_length<2: raise ValueError("BOS/EOS를 포함하려면 max_length>=2")
            if len(tokens)>max_length:
                tokens=tokens[:max_length-1]+["[EOS]"]
                truncated=True
        valid=len(tokens)
        if padding_to is not None:
            if padding_to<valid: raise ValueError("padding_to must be >= valid length")
            tokens=tokens+["[PAD]"]*(padding_to-valid)
        ids=[self.vocab.get(t,self.vocab["[UNK]"]) for t in tokens]
        mask=[0 if t=="[PAD]" else 1 for t in tokens]
        return {"tokens":tokens,"input_ids":ids,"attention_mask":mask,
                "valid_length":valid,"truncated":truncated,"original_length":len(raw)+2}

    def batch(self, texts, max_length=None):
        items=[self.encode(t,max_length=max_length) for t in texts]
        max_size=max(len(i["input_ids"]) for i in items)
        return [self.encode(t,max_length=max_length,padding_to=max_size) for t in texts]

def context_budget(window, parts:dict, output_reserved:int):
    used=sum(parts.values())
    return {"window":window,"input_used":used,"output_reserved":output_reserved,
            "remaining":window-used-output_reserved,
            "fits":used+output_reserved<=window}

def cosine(a,b):
    a=torch.as_tensor(a,dtype=torch.float32)
    b=torch.as_tensor(b,dtype=torch.float32)
    return float(torch.nn.functional.cosine_similarity(a,b,dim=0))

def attention(q,k,v,causal=True):
    q=torch.as_tensor(q,dtype=torch.float32)
    k=torch.as_tensor(k,dtype=torch.float32)
    v=torch.as_tensor(v,dtype=torch.float32)
    scores=q@k.T/math.sqrt(q.shape[-1])
    mask=torch.triu(torch.ones_like(scores,dtype=torch.bool),diagonal=1)
    weights=torch.softmax(scores.masked_fill(mask,float('-inf')) if causal else scores,dim=-1)
    return scores,weights,weights@v,mask

def write_json(path, data):
    p=Path(path);p.parent.mkdir(exist_ok=True,parents=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

def write_md(path,text):
    p=Path(path);p.parent.mkdir(exist_ok=True,parents=True)
    p.write_text(text,encoding='utf-8')

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))
