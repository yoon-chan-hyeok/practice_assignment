from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import KnowledgeRead, KnowledgeWrite
from app.services import knowledge_service as service

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])

def to_read(item) -> KnowledgeRead:
    return KnowledgeRead(id=item.id, title=item.title, content=item.content, category=item.category.name)

@router.get("", response_model=list[KnowledgeRead])
def list_knowledge(category: str | None = Query(default=None), db: Session = Depends(get_db)):
    return [to_read(x) for x in service.list_knowledge(db, category)]

@router.get("/{knowledge_id}", response_model=KnowledgeRead)
def read_knowledge(knowledge_id: int, db: Session = Depends(get_db)):
    return to_read(service.get_knowledge(db, knowledge_id))

@router.post("", response_model=KnowledgeRead, status_code=status.HTTP_201_CREATED)
def create_knowledge(payload: KnowledgeWrite, db: Session = Depends(get_db)):
    # TODO H12: Router가 Service 결과를 응답 모델로 변환하게 하세요.
    raise NotImplementedError("TODO H12")

@router.put("/{knowledge_id}", response_model=KnowledgeRead)
def update_knowledge(knowledge_id: int, payload: KnowledgeWrite, db: Session = Depends(get_db)):
    return to_read(service.update_knowledge(db, knowledge_id, payload))

@router.delete("/{knowledge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_knowledge(knowledge_id: int, db: Session = Depends(get_db)) -> Response:
    service.delete_knowledge(db, knowledge_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
