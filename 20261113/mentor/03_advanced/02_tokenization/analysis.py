from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
LEVEL_ROOT = HERE.parent
sys.path.insert(0, str(LEVEL_ROOT))  # 어느 작업 폴더에서 실행해도 common 패키지를 찾습니다.
from common.support import DATA, ToyTokenizer, context_budget, write_json

# 주의: 여기의 ToyTokenizer는 규칙 기반 학습용이며 실제 BERT 서브워드 출력과 다릅니다.
def run_analysis():
    texts = [item["content"] for item in DATA]
    tok = ToyTokenizer(texts + ["AI", "FastAPI와 PostgreSQL", "print(x) // code"])

    # BEGIN D20-02-A01
    rows=[]
    for item in DATA:
        record=tok.encode(item["content"])
        rows.append({"id":item["id"], "text":item["content"],
                     "tokens":record["tokens"], "ids":record["input_ids"],
                     "count":record["valid_length"],"special_count":2})
    # 해설: [BOS]/[EOS]는 이 교육용 토크나이저의 규칙이며 실제 모델마다 다릅니다.
    # END D20-02-A01

    # BEGIN D20-02-A02
    batch = tok.batch(["AI", "FastAPI와 PostgreSQL"])
    # 해설: batch의 모든 input_ids 길이는 같고 [PAD] 위치의 attention_mask는 0입니다.
    assert len(batch[0]["input_ids"]) == len(batch[1]["input_ids"])
    assert all(len(b["input_ids"]) == len(b["attention_mask"]) for b in batch)
    # END D20-02-A02

    # BEGIN D20-02-A03
    budget=context_budget(5000,{"system":300,"history":1200,"evidence":2000,"user":150},850)
    # 해설: 입력 3,650 + 출력 예약 850 = 4,500; 예시 창 5,000에서 500 남음.
    # END D20-02-A03

    # BEGIN D20-02-A04
    trunc_cases={
        str(n):tok.encode("FastAPI와 PostgreSQL",max_length=n)
        for n in (5,12)
    }
    # 해설: max_length는 이 예제에서 BOS/EOS를 포함한 입력 상한입니다.
    # END D20-02-A04

    # BEGIN D20-02-A05
    batch_report=[{
        "valid":it["valid_length"], "padded":len(it["input_ids"]),
        "pad_positions":[i for i,v in enumerate(it["attention_mask"]) if v==0],
    } for it in batch]
    # END D20-02-A05

    # BEGIN D20-02-A06
    mixed = ["실습 파일은 개인 폴더에 보관합니다.",
             "Keep files in your own folder.", "print(x) # debug"]
    # 미등록 단어는 [UNK]가 될 수 있으므로, 해석할 때 어휘표 고정 여부를 고려합니다.
    mixed_rows=[{"text":text,**tok.encode(text)} for text in mixed]
    # END D20-02-A06

    # BEGIN D20-02-A07
    small_budget=context_budget(4096,{"system":300,"history":1200,"evidence":2000,"user":150},850)
    assert not small_budget["fits"]
    policy="초과 시 검색 근거 또는 이전 대화량을 줄이고, 출력 예약은 별도로 관리"
    # END D20-02-A07

    # BEGIN D20-02-A08
    result={"tokenizer_kind":"교육용 regex·고정 어휘표 (사전학습 모델이 아님)",
            "records":rows,"batch":batch,"budget":budget,"truncation":trunc_cases,
            "batch_report":batch_report,"language_comparison":mixed_rows,
            "overflow_budget":small_budget,"policy":policy}
    write_json(HERE/"outputs"/"token_report.json",result)
    print("[02]",[(x["id"],x["count"]) for x in rows],"remaining",budget["remaining"])
    # END D20-02-A08

