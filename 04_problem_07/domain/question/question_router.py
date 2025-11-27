# question_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Question
from domain.question.question_schema import QuestionSubject

router = APIRouter(
    prefix='/api/question',
    tags=['question'],
)


@router.get('/', response_model=list[QuestionSubject])
def question_list(db: Session = Depends(get_db)):
    """
    Question 테이블 전체 목록을 조회해서
    QuestionSubject 스키마 리스트로 반환한다.
    """
    questions = db.query(Question).all()
    return questions
