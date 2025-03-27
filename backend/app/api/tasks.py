from datetime import datetime, timedelta
from sqlalchemy import Date
from fastapi import Depends, HTTPException,status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.requests import Request
from uuid import UUID, uuid4
from database.models.tasks import Task
from database.psql import get_db
from crud.tasks import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/add_task", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_task(id: UUID, deadline, deskription: str, db: Session = Depends(get_db)) -> dict[str, any]:
    try:
        task = TaskService.create_task(db, id, deadline, deskription)
        # Создаем словарь для возврата данных
        response_data = {
            "id": task.task_id,  # Преобразуем UUID в строку
            "user_id": task.user_id, 
            "deadline": task.deadline,
            "deskription": task.description  # Преобразуем datetime в строку ISO 8601
        }
        return response_data
    except HTTPException as e:
        raise e  # Пробрасываем HTTPException дальше
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    


@router.get("/read_task")
async def read_task(task_id: int, db: Session = Depends(get_db)):
    try:
        task = TaskService.read_task(db, task_id)
    except HTTPException as e:
        raise HTTPException(status_code=404, detail="Task not found")
    response_data = {
        "id": task.task_id,  # Преобразуем UUID в строку
        "user_id": task.user_id, 
        "deadline": task.deadline,
        "deskription": task.description  # Преобразуем datetime в строку ISO 8601
        }
    return response_data

@router.delete("/del_task")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    try:
        TaskService.delete_task(db, task_id)
    except HTTPException as e:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


@router.patch("/update_task", response_model=None, status_code=status.HTTP_201_CREATED)
async def update_task(id: int, deadline, deskription: str, db: Session = Depends(get_db)) -> dict[str, any]:
    try:
        task = TaskService.update_task(db, id, deadline, deskription)
        # Создаем словарь для возврата данных
        response_data = {
            "id": task.task_id,  # Преобразуем UUID в строку
            "user_id": task.user_id, 
            "deadline": task.deadline,
            "deskription": task.description  # Преобразуем datetime в строку ISO 8601
        }
        return response_data
    except HTTPException as e:
        raise e  # Пробрасываем HTTPException дальше
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
