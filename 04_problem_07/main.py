# main.py
from fastapi import FastAPI
from database import Base, engine
from domain.question.question_router import router as question_router

app = FastAPI()

# ⭐ 아주 중요! 테이블 생성하는 코드
Base.metadata.create_all(bind=engine)

app.include_router(question_router)
