class KnowledgeNotFoundError(Exception):
    def __init__(self, knowledge_id: int): self.knowledge_id = knowledge_id

class DataConflictError(Exception):
    def __init__(self, message: str): self.message = message
