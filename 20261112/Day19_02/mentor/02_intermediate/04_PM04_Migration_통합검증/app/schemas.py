from pydantic import BaseModel, Field

# 강사 해설: 외부 API 계약은 title/content/category 문자열을 유지하고 내부 FK 숫자는 숨깁니다.
class KnowledgeWrite(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1, max_length=2000)
    category: str = Field(min_length=1, max_length=30)

class KnowledgeRead(KnowledgeWrite):
    id: int
