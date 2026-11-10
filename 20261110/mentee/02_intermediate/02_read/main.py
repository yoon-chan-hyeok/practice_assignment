"""JSON 목록·상세 조회. 실행: python -m uvicorn main:app --reload"""
from fastapi import FastAPI, HTTPException, Response
from storage import LOCK, read_data, write_data

app = FastAPI(title="Knowledge API", description="AI 플랫폼의 원본 지식 관리 연습")

@app.get("/health")
def health():
    # 이 경로의 응답 확인입니다. 파일·DB·AI 모델의 전체 상태 점검은 아닙니다.
    return {"status": "ok"}

@app.get("/hello")
def hello(name: str = "수강생"):
    return {"message": f"안녕하세요, {name}"}

@app.get("/api/knowledge")
def list_knowledge(category: str | None = None):
    with LOCK:
        data = read_data()
    result = data["entries"]
    if category is not None:
        # BEGIN A02-01
        # TODO A02-01: category와 정확히 일치하는 항목만 result에 남기세요. 일치 항목이 없으면 빈 목록이어야 합니다.
        # 힌트: for 반복문으로 새 목록을 만들어도 됩니다.
        # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
        raise NotImplementedError("A02-01를 먼저 완성하세요.")
        # END A02-01
    # 조건에 맞는 지식이 없으면 정상 조회 200과 빈 배열 []입니다.
    return result

@app.get("/api/knowledge/{knowledge_id}")
def get_knowledge(knowledge_id: int):
    with LOCK:
        data = read_data()
    # BEGIN A02-02
    # TODO A02-02: entries를 순회하여 id가 knowledge_id인 지식을 반환하세요. 찾지 못하면 반복문 다음으로 진행하세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    raise NotImplementedError("A02-02를 먼저 완성하세요.")
    # END A02-02
    # 입력은 정수이지만 저장된 항목이 없으면 404입니다. foo 같은 Path는 먼저 422입니다.
    # BEGIN A02-03
    # TODO A02-03: 반복문에서 찾지 못한 경우 HTTPException으로 404와 Knowledge not found를 전달하세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    raise NotImplementedError("A02-03를 먼저 완성하세요.")
    # END A02-03
