# -*- coding: utf-8 -*-
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse
from model import TodoItem
from typing import List, Dict
import csv
import os

app = FastAPI()
router = APIRouter()

CSV_FILE = 'todo.csv'


def read_csv() -> List[Dict[str, str]]:
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        return list(reader)


def write_csv_all(data: List[Dict[str, str]]) -> None:
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8-sig') as file:
        fieldnames = ['task', 'priority']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def append_csv(item: Dict[str, str]) -> None:
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=['task', 'priority'])
        if not file_exists:
            writer.writeheader()
        writer.writerow(item)


@router.post('/add_todo')
async def add_todo(request: Request) -> JSONResponse:
    data = await request.json()
    if not data or not data.get('task') or not data.get('priority'):
        return JSONResponse({'error': '입력 값이 비어있습니다.'}, media_type='application/json; charset=utf-8')
    append_csv({'task': data['task'], 'priority': data['priority']})
    return JSONResponse({'message': '할 일이 추가되었습니다.'}, media_type='application/json; charset=utf-8')


@router.get('/retrieve_todo')
async def retrieve_todo() -> JSONResponse:
    todos = read_csv()
    return JSONResponse({'todos': todos}, media_type='application/json; charset=utf-8')


@router.get('/get_single_todo/{todo_id}')
async def get_single_todo(todo_id: int) -> JSONResponse:
    todos = read_csv()
    if 0 <= todo_id < len(todos):
        return JSONResponse(todos[todo_id], media_type='application/json; charset=utf-8')
    return JSONResponse({'error': '해당 ID의 항목이 존재하지 않습니다.'}, status_code=404)


@router.put('/update_todo/{todo_id}')
async def update_todo(todo_id: int, item: TodoItem) -> JSONResponse:
    todos = read_csv()
    if 0 <= todo_id < len(todos):
        todos[todo_id] = {'task': item.task, 'priority': item.priority}
        write_csv_all(todos)
        return JSONResponse({'message': '할 일이 수정되었습니다.'}, media_type='application/json; charset=utf-8')
    return JSONResponse({'error': '해당 ID의 항목이 존재하지 않습니다.'}, status_code=404)


@router.delete('/delete_single_todo/{todo_id}')
async def delete_single_todo(todo_id: int) -> JSONResponse:
    todos = read_csv()
    if 0 <= todo_id < len(todos):
        deleted = todos.pop(todo_id)
        write_csv_all(todos)
        return JSONResponse({'message': '삭제 완료', 'deleted': deleted}, media_type='application/json; charset=utf-8')
    return JSONResponse({'error': '해당 ID의 항목이 존재하지 않습니다.'}, status_code=404)


app.include_router(router)
