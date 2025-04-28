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
from app.services import group_service

from backend.app.api.depencies.services import get_group_service
from backend.app.shemas.groups import GroupID

router = APIRouter(prefix="/students", tags=["students"])

# Что хотим уметь для сущности студента?
# 1.1 ++ - получать номер группы для конкретного студента (вход - имя студента, выход - номер группы )(только для авторизованных)
# 1.2 ++ - получать номер группы для себя (вход - ничего, получаем id юзера через токен, выход - номер группы)
# 2 - -- (админ) добавлять/изменять номер группы (а вообще - и параметры в целом) для конкретного студента (вход - id, номер группы, выход - успех/неуспех, только для админа??)
# 2.2 ++ добавлять/изменять номер группы (а вообще - и параметры в целом) для себя (вход - новый номер группы, получаем id юзера через токен, выход - успех/неуспех)
# 3 - ++  получать список всех студентов (вход - ничего, выход - список из (имя_студента, номер группы), для авторизованного пользователя)
# 4.1 - ++ получать список студентов по конкретной группе (вход - номер группы, выход - список из студентов)
# 4.2 - получать список студентов своей группы (вход - получаем id юзера через токен, выход - список из студентов)
# 5 ++ "/register_student" - создавать студента (себя) (вход - получаем id usera по токену + номер группы, выход - успех/неуспех) - должно ли подтверждаться админом?
# 6.1 ++ "/delete_me"- удалять студента (себя) (вход - получаем id usera по токену, выход - успех/неуспех)
# 6.2 ++ "/delete_user"- удалять конкретного студента (вход - id юзера, выход - успех/неуспех) - только для админа


@router.post("/register_student", response_model=StudentBase,
             status_code=status.HTTP_201_CREATED,
             summary='Register a new student',
             description='Create a new student in database. Requre user id and group id.\n')
async def create_student(group_number: StudentIn, student: UserOut = Depends(get_current_user), service = Depends(get_student_service), group_service = Depends(get_group_service)):
    #получить id группы по номеру группы
    group_id = await  group_service.get_by_number(group_number)
    #создать new student, провалидировать по user_base
    new_student = StudentBase.model_validate({"student_id": student.id, "group_id": group_id})
    return await service._create_student(new_student)

@router.delete("/delete_me",
             status_code=status.HTTP_200_OK,
             summary='Delete current student',
             description='Delete current student.\n')
async def delete_me(student = Depends(get_current_user), service = Depends(get_student_service)):

    return await service.delete_student(student.id)


@router.delete("/delete_student",
             status_code=status.HTTP_200_OK,
             summary='Delete student',
             description='Delete any student. This is only for admins\n',
             dependencies=[Depends(require_role(1))]
             )
async def delete_student(student_id: int, service = Depends(get_student_service)):
    return await service.delete_student(student_id)

@router.post("/get_my_group",
             status_code=status.HTTP_200_OK,
             summary='Get group number for current student',
             description='Get group number for current student.\n')
async def get_my_group(student: UserOut = Depends(get_current_user), service = Depends(get_student_service), group_service = Depends(get_group_service)):
    group_id = await service.get_group(student.id)
    #Получение номера группы по id
    validate_group_id = GroupID.model_validate({"group_id": group_id})
    group_number =  await  group_service.get_by_id(validate_group_id)
    return group_number


@router.get("/get_group_num/{student_id}",
             status_code=status.HTTP_200_OK,
             summary='Get group number any student',
             description='Get group number any student by his ID (late may be change for name).\n',
             dependencies=[Depends(get_current_user)])
async def get_user_group(student_id: int, service = Depends(get_student_service), group_service = Depends(get_group_service)):
    student_id = StudentID.model_validate({"student_id": student_id})
    group_id = await service.get_group(student_id.student_id)
    validate_group_id = GroupID.model_validate({"group_id": group_id})
    group_number = await  group_service.get_by_id(validate_group_id)
    return group_number


@router.patch("/update_my_group",
             status_code=status.HTTP_200_OK,
             summary='Update group number for current student',
             description='Update group number for current student.\n')
async def update_my_group(group_number: GroupNumber, student: UserOut = Depends(get_current_user), service = Depends(get_student_service), group_service = Depends(get_group_service)):
    group_id = await group_service.get_by_number(group_number)
    return await service.update_group(student.id, group_id)

@router.get("/get_all_students",
             status_code=status.HTTP_200_OK,
             summary='Get the list of all students',
             description='Get the list of all students.\n')
async def get_all(dependencies = Depends(get_current_user), service = Depends(get_student_service), group_service = Depends(get_group_service)):
    students_and_group_id = await service.get_all()
    students = []
    print ( students_and_group_id)
    for student in students_and_group_id:
        #Перевод id в номер группы
        group_id = await service.get_group(student['id'])
        validate_group_id = GroupID.model_validate({"group_id": group_id})
        group_number = await  group_service.get_by_id(validate_group_id)
        students.append({'id': student['id'], 'group_num': group_number })
        print(student)
    return students



@router.get("/get_student_by_group/{group_num}",
             status_code=status.HTTP_200_OK,
             summary='Get the list of students for group',
             description='Get the list of students for group.\n')
async def get_students_by_group(group_num: str, dependencies = Depends(get_current_user), service = Depends(get_student_service), group_service = Depends(get_group_service)):
    group_number = StudentIn.model_validate({"group_number": group_num})
    # Получение id группы по номеру
    group_id = await  group_service.get_by_number(group_number)
    return await service.get_by_group(int(group_id))


@router.get("/get_my_groupmates",
             summary='Get students from group of current user',
             description='Get students from group of current user.\n')
async def get_my_groupmates(student: UserOut = Depends(get_current_user), service = Depends(get_student_service)):
    #Получение номера группы студента по его id
    group_id = await service.get_group(student.id)
    #Получение студентов по id группы
    return await service.get_by_group(group_id)

