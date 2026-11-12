from fastapi import FastAPI, HTTPException, Response
from storage import LOCK, read_data, write_data
from schemas import Knowledge, KnowledgeWrite
from queries import filter_entries, find_entry

app = FastAPI(title="Day19 AM Knowledge API - Applied")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/knowledge", response_model=list[Knowledge])
def list_knowledge(category: str | None = None):
    with LOCK:
        data = read_data()
    # BEGIN A-API-03
    # 해설 A-API-03: read_data()의 entries와 category를 filter_entries에 전달하여 결과를 반환하세요.
    return filter_entries(data["entries"], category)
    # END A-API-03
@app.get("/api/knowledge/{knowledge_id}", response_model=Knowledge)
def get_knowledge(knowledge_id: int):
    with LOCK:
        data = read_data()
    # BEGIN A-API-04
    # 해설 A-API-04: find_entry에 data의 entries와 knowledge_id를 전달해 entry를 구하세요.
    entry = find_entry(data["entries"], knowledge_id)
    # END A-API-04
    # BEGIN A-API-05
    # 해설 A-API-05: entry가 None이면 HTTPException(404, "Knowledge not found")을
    # raise하고, 있으면 반환하세요.
    if entry is None:
        raise HTTPException(404, "Knowledge not found")
    return entry
    # END A-API-05
@app.post("/api/knowledge", status_code=201, response_model=Knowledge)
def create_knowledge(payload: KnowledgeWrite):
    with LOCK:
        data = read_data()
        # BEGIN A-API-06
        # 해설 A-API-06: payload를 dict로 변환하고 next_id를 id로 부여한 entry를 만드세요.
        entry = payload.model_dump()
        entry["id"] = data["next_id"]
        # END A-API-06
        # BEGIN A-API-07
        # 해설 A-API-07: entry를 추가하고 next_id를 증가시킨 뒤 파일에 저장하세요.
        data["entries"].append(entry)
        data["next_id"] += 1
        write_data(data)
        # END A-API-07
    return entry

@app.put("/api/knowledge/{knowledge_id}", response_model=Knowledge)
def update_knowledge(knowledge_id: int, payload: KnowledgeWrite):
    with LOCK:
        data = read_data()
        # BEGIN A-API-08
        # 해설 A-API-08: 같은 ID의 항목만 입력 세 필드로 교체하고 저장·반환하세요. 끝까지 없으면 잠금 블록 밖의 404로 진행합니다.
        for i, entry in enumerate(data["entries"]):
            if entry["id"] == knowledge_id:
                updated = payload.model_dump()
                updated["id"] = knowledge_id
                data["entries"][i] = updated
                write_data(data)
                return updated
        # END A-API-08
    raise HTTPException(404, "Knowledge not found")

@app.delete("/api/knowledge/{knowledge_id}", status_code=204)
def delete_knowledge(knowledge_id: int):
    with LOCK:
        data = read_data()
        # BEGIN A-API-09
        # 해설 A-API-09: 같은 ID의 항목 하나만 삭제·저장한 뒤 Response(status_code=204)를 반환하세요. 없으면 이후
        # 404로 진행합니다.
        for i, entry in enumerate(data["entries"]):
            if entry["id"] == knowledge_id:
                data["entries"].pop(i)
                write_data(data)
                return Response(status_code=204)
        # END A-API-09
    raise HTTPException(404, "Knowledge not found")
