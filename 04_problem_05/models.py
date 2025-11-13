from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base
import datetime

class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
