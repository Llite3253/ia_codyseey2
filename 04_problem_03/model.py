from pydantic import BaseModel

class TodoItem(BaseModel):
    task: str
    priority: str
