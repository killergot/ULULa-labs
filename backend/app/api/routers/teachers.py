from app.api.depencies.guard import get_current_id, get_current_user, require_role
from app.api.depencies.services import get_student_service
from app.shemas.students import StudentBase, StudentIn, StudentID
from app.shemas.groups import GroupNumber
from app.shemas.auth import UserOut
from fastapi import Depends, status
from fastapi.routing import APIRouter
from app.database.models.students import Student
from app.database.models.groups import Group
from app.services import student_service
from app.services import teacher_service

from app.api.depencies.services import get_teacher_service
from app.shemas.groups import GroupID

router = APIRouter(prefix="/teachers", tags=["teachers"])

# Что хотим уметь для сущности студента?
# 1.1 ++ - получать номер группы для конкретного студента (вход, выход - номер группы )(только для авторизованных)
# 1.2 ++ - получать номер группы для себя (вход - ничего, получаем id юзера через токен, выход - номер группы)
# 2 - -- (админ) добавлять/изменять номер группы (а вообще - и параметры в целом) для конкретного студента (вход - id, номер группы, выход - успех/неуспех, только для админа??)
# 2.2 ++ добавлять/изменять номер группы (а вообще - и параметры в целом) для себя (вход - новый номер группы, получаем id юзера через токен, выход - успех/неуспех)
# 3 - ++  получать список всех студентов (вход - ничего, выход - список из (имя_студента, номер группы), для авторизованного пользователя)
# 4.1 - ++ получать список студентов по конкретной группе (вход - номер группы, выход - список из студентов)
# 4.2 - получать список студентов своей группы (вход - получаем id юзера через токен, выход - список из студентов)
# 5 ++ "/register_student" - создавать студента (себя) (вход - получаем id usera по токену + номер группы, выход - успех/неуспех) - должно ли подтверждаться админом?
# 6.1 ++ "/delete_me"- удалять студента (себя) (вход - получаем id usera по токену, выход - успех/неуспех)
# 6.2 ++ "/delete_user"- удалять конкретного студента (вход - id юзера, выход - успех/неуспех) - только для админа


@router.post("/register_teacher",
             status_code=status.HTTP_201_CREATED,
             summary='Register a new teacher',
             description='Create a new teacher in database. Requre user id and FIO.\n')
async def create_student(FIO: str, teacher: UserOut = Depends(get_current_user), service = Depends(get_teacher_service)):
    new_teacher = ({"teacher_id": teacher.id, "FIO": FIO})
    return await service.create_teacher(new_teacher)


