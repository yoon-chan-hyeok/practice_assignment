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
    # TODO B-API-01: data의 entries를 id 오름차순으로 반환하세요. sorted(..., key=lambda e:
    # e["id"])를 사용할 수 있습니다. next_id는 응답하지 않습니다.
    raise NotImplementedError("B-API-01: 주석 요구사항을 완성하세요.")
    # END B-API-01
@app.get("/api/knowledge/{knowledge_id}", response_model=Knowledge)
def get_knowledge(knowledge_id: int):
    with LOCK:
        data = read_data()
    for entry in data["entries"]:
        # BEGIN B-API-02
        # TODO B-API-02: 반복 중인 entry의 id가 knowledge_id와 같을 때 entry를 반환하세요. 목록 인덱스와 ID를
        # 혼동하지 마세요.
        raise NotImplementedError("B-API-02: 주석 요구사항을 완성하세요.")
        # END B-API-02
    raise HTTPException(404, "Knowledge not found")

@app.post("/api/knowledge", status_code=201, response_model=Knowledge)
def create_knowledge(payload: KnowledgeWrite):
    with LOCK:
        data = read_data()
        # BEGIN B-API-03
        # TODO B-API-03: payload를 dict로 변환하여 entry에 넣고, data의 next_id 값을 entry의 id로
        # 넣으세요.
        raise NotImplementedError("B-API-03: 주석 요구사항을 완성하세요.")
        # END B-API-03
        # BEGIN B-API-04
        # TODO B-API-04: entry를 entries에 추가하고 next_id를 1 늘린 뒤 write_data(data)로 저장하세요.
        raise NotImplementedError("B-API-04: 주석 요구사항을 완성하세요.")
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
                # TODO B-API-05: 찾은 위치 i의 항목을 updated로 교체한 뒤 저장하세요. 같은 ID를 유지하고 다른 항목은 변경하지
                # 않습니다.
                raise NotImplementedError("B-API-05: 주석 요구사항을 완성하세요.")
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
                # TODO B-API-06: 찾은 위치 i의 항목 하나만 삭제하고 저장하세요. next_id는 줄이지 않습니다.
                raise NotImplementedError("B-API-06: 주석 요구사항을 완성하세요.")
                # END B-API-06
                return Response(status_code=204)
    raise HTTPException(404, "Knowledge not found")
