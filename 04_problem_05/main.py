from fastapi import FastAPI
from database import Base, engine

app = FastAPI()

# 테이블이 없으면 생성
Base.metadata.create_all(bind=engine)

@app.get('/')
def read_root():
    return {'message': 'Hello FastAPI Board!'}
