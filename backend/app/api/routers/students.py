from datetime import datetime, timedelta

from fastapi import Depends, HTTPException,status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.requests import Request
from uuid import UUID, uuid4
from app.database.models.students import Student
from app.database.psql import get_db
from app.crud.students import StudentService

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/add_group", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_student(id: UUID, group_number: str, db: Session = Depends(get_db)) -> dict[str, any]:
    try:
        user_group = StudentService.create_student(db, id, group_number)
        # Создаем словарь для возврата данных
        response_data = {
            "id": str(user_group.id),  # Преобразуем UUID в строку
            "group_number": user_group.group_number,
            "created_at": user_group.created_at.isoformat()  # Преобразуем datetime в строку ISO 8601
        }
        return response_data
    except HTTPException as e:
        raise e  # Пробрасываем HTTPException дальше
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    

@router.get("/read_student")
async def read_schedule(id: UUID, db: Session = Depends(get_db)):
    try:
        student = StudentService.is_student_exist(db, id)
    except HTTPException as e:
        raise HTTPException(status_code=404, detail="Student not found")
    if student: 
        return student
    else: 
        response_data = {
            "Result: this student not exist(("
        }
    return response_data 
@router.post("/update_group", response_model=None, status_code=status.HTTP_201_CREATED)
async def update_student(id: UUID, group_number: str, db: Session = Depends(get_db)) -> dict[str, any]:
    try:
        user_group = StudentService.create_student(db, id, group_number)
        # Создаем словарь для возврата данных
        response_data = {
            "id": str(user_group.id),  # Преобразуем UUID в строку
            "group_number": user_group.group_number,
            "created_at": user_group.created_at.isoformat()  # Преобразуем datetime в строку ISO 8601
        }
        return response_data
    except HTTPException as e:
        raise e  # Пробрасываем HTTPException дальше
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    

@router.delete("/del_student")
async def delete_student(id: UUID, db: Session = Depends(get_db)):
    try:
        StudentService.delete_student(db, id)
    except HTTPException as e:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Student deleted successfully"}