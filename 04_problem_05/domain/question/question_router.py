from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Question

router = APIRouter(
    prefix='/api/question'
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/')
def question_list(db: Session = Depends(get_db)):
    questions = db.query(Question).all()
    return questions
