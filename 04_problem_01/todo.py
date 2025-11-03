from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse
from typing import Dict, List

app = FastAPI()
router = APIRouter()

# todo 항목을 임시로 저장할 리스트 (메모리 기반)
todo_list: List[Dict[str, str]] = []

@router.post('/add_todo')
async def add_todo(request: Request) -> JSONResponse:
    data = await request.json()
    # 유효성 검사: task와 priority가 존재해야 함
    if not data or not data.get('task') or not data.get('priority'):
        return JSONResponse(
            content={'error': '입력 값이 비어있습니다.'},
            media_type='application/json; charset=utf-8'
        )
    # 리스트에 추가
    todo_list.append({'task': data['task'], 'priority': data['priority']})
    return JSONResponse(
        content={'message': '할 일이 추가되었습니다.'},
        media_type='application/json; charset=utf-8'
    )

@router.get('/retrieve_todo')
async def retrieve_todo() -> JSONResponse:
    return JSONResponse(
        content={'todos': todo_list},
        media_type='application/json; charset=utf-8'
    )

# 라우터 등록
app.include_router(router)
