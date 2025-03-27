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