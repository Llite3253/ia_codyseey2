# domain/question/question_schema.py
from pydantic import BaseModel

class QuestionBase(BaseModel):
    subject: str
    content: str

class QuestionSubject(BaseModel):
    id: int
    subject: str

    class Config:
        orm_mode = True   # 보너스 과제에서 True/False 바꿔보면 됨
