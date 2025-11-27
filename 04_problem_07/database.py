# database.py

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = 'sqlite:///./board.db'

engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ★ 여기 추가해야 함 ★
Base = declarative_base()


@contextmanager
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db():
    with db_session() as db:
        yield db
