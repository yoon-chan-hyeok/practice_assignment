from fastapi import FastAPI, HTTPException, Response
from storage import LOCK, read_data, write_data

from pydantic import BaseModel, Field


class KnowledgeWrite(BaseModel):
    # 세 필드는 모두 필수입니다. 길이 규칙은 공백 제거 규칙과 다릅니다.
    title: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1, max_length=2000)
    category: str = Field(min_length=1, max_length=30)


class Knowledge(KnowledgeWrite):
    id: int

app = FastAPI(title="Day19 AM Knowledge API - Basic")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/knowledge", response_model=list[Knowledge])
def list_knowledge():
    with LOCK:
        data = read_data()
    # BEGIN B-API-01
    # 해설 B-API-01: 파일 전체가 아니라 사용자용 entries 배열을 반환합니다. JSON의 next_id는 다음 ID 발급을 위한
    # 내부 상태입니다.
    return sorted(data["entries"], key=lambda e: e["id"])
    # END B-API-01
@app.get("/api/knowledge/{knowledge_id}", response_model=Knowledge)
def get_knowledge(knowledge_id: int):
    with LOCK:
        data = read_data()
    for entry in data["entries"]:
        # BEGIN B-API-02
        # 해설 B-API-02: 반복 중인 entry의 id가 knowledge_id와 같을 때 entry를 반환하세요. 목록 인덱스와 ID를
        # 혼동하지 마세요.
        if entry["id"] == knowledge_id:
            return entry
        # END B-API-02
    raise HTTPException(404, "Knowledge not found")

@app.post("/api/knowledge", status_code=201, response_model=Knowledge)
def create_knowledge(payload: KnowledgeWrite):
    with LOCK:
        data = read_data()
        # BEGIN B-API-03
        # 해설 B-API-03: payload를 dict로 변환하여 entry에 넣고, data의 next_id 값을 entry의 id로
        # 넣으세요.
        entry = payload.model_dump()
        entry["id"] = data["next_id"]
        # END B-API-03
        # BEGIN B-API-04
        # 해설 B-API-04: 추가와 다음 번호를 같은 파일에 저장합니다. 삭제 가능한 목록에서는 len(entries)+1로 ID를 만들지
        # 않습니다.
        data["entries"].append(entry)
        data["next_id"] += 1
        write_data(data)
        # END B-API-04
    return entry

@app.put("/api/knowledge/{knowledge_id}", response_model=Knowledge)
def update_knowledge(knowledge_id: int, payload: KnowledgeWrite):
    with LOCK:
        data = read_data()
        for i, entry in enumerate(data["entries"]):
            if entry["id"] == knowledge_id:
                updated = payload.model_dump()
                updated["id"] = knowledge_id
                # BEGIN B-API-05
                # 해설 B-API-05: 찾은 위치 i의 항목을 updated로 교체한 뒤 저장하세요. 같은 ID를 유지하고 다른 항목은 변경하지
                # 않습니다.
                data["entries"][i] = updated
                write_data(data)
                # END B-API-05
                return updated
    raise HTTPException(404, "Knowledge not found")

@app.delete("/api/knowledge/{knowledge_id}", status_code=204)
def delete_knowledge(knowledge_id: int):
    with LOCK:
        data = read_data()
        for i, entry in enumerate(data["entries"]):
            if entry["id"] == knowledge_id:
                # BEGIN B-API-06
                # 해설 B-API-06: 한 항목만 삭제하고 저장한 뒤 바깥의 Response로 빈 204를 반환합니다. 목록 전체를 비우거나
                # next_id를 감소시키지 않습니다.
                data["entries"].pop(i)
                write_data(data)
                # END B-API-06
                return Response(status_code=204)
    raise HTTPException(404, "Knowledge not found")
