from datetime import datetime, timedelta

#from numpy.doc.constants import new_lines

from app.api.depencies.services import get_student_service
from app.shemas.students import StudentBase, StudentIn
from fastapi import Depends, HTTPException,status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.requests import Request
from uuid import UUID, uuid4
from app.database.models.students import Student
#from app.database.psql import get_db
from app.crud.students import StudentService

router = APIRouter(prefix="/students", tags=["students"])

# Что хотим уметь для сущности студента?
# 1.1 - получать номер группы для конкретного студента (вход - имя студента, выход - номер группы )(только для авторизованных)
# 1.2 - получать номер группы для себя (вход - ничего, получаем id юзера через токен, выход - номер группы)
# 2 - добавлять/изменять номер группы (а вообще - и параметры в целом) для конкретного студента (вход - id, номер группы, выход - успех/неуспех, только для админа??)
# 2.2 добавлять/изменять номер группы (а вообще - и параметры в целом) для себя (вход - новый номер группы, получаем id юзера через токен, выход - успех/неуспех)
# 3 - получать список всех студентов (вход - ничего, выход - список из (имя_студента, номер группы), для авторизованного пользователя)
# 4.1 - получать список студентов по конкретной группе (вход - номер группы, выход - список из студентов)
# 4.2 - получать список студентов своей группы (вход - получаем id юзера через токен, выход - список из студентов)
# 5 - создавать студента (себя) (вход - получаем id usera по токену + номер группы, выход - успех/неуспех) - должно ли подтверждаться админом?
# 6.1 - удалять студента (себя) (вход - получаем id usera по токену, выход - успех/неуспех)
# 6.2 - удалять конкретного студента (вход - id юзера, выход - успех/неуспех) - только для админа


@router.post("/register_student", response_model=StudentBase,
             status_code=status.HTTP_201_CREATED,
             summary='Register a new student',
             description='Create a new student in database. Requre user id and group id.\n')
async def create_student(student: StudentIn, service: StudentService = Depends(get_student_service)):
    #получить id группы по номеру группы
    #заглушка
    group_id = 5126456
    #создать new student, провалидировать по user_base
    new_student = StudentBase.model_validate({'student_id': student.student_id, 'group_id': group_id})
    return await service.create_student(new_student)


"""
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
"""