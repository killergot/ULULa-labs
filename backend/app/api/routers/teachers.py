from idlelib.query import Query

from attr.validators import min_len
from watchfiles import awatch
from typing import Optional

from app.database.models.achievent import Achievement
from app.api.depencies.guard import get_current_user, require_role
from app.services.teacher_service import TeacherService
from app.shemas.teachers import FIO, WeekNumber, TeacherUpdateIn
from app.shemas.teacher_subject import SubjectName, TeacherSubjectBase
from app.shemas.auth import UserOut
from app.shemas.achievements import AchieveIn, AchieveID, AchieveUpdate
from app.shemas.labs import LabWorkIn, LabWorkID
from app.shemas.assignments import AssignmentsIn, AssignmentID
from fastapi import Depends, status, Query
from fastapi.routing import APIRouter
from app.api.depencies.services import get_teacher_service
from app.api.depencies.services import get_student_service
from app.api.depencies.validation import get_week_number, get_FIO, get_achieve_id, get_lab_work_id
from app.services.role_service import ADMIN_ROLE
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


@router.post("/register",
             status_code=status.HTTP_201_CREATED,
             summary='Register current user as a teacher',
             description='Create a new teacher in database. Requre FIO.\n')
async def create_student(FIO: str, teacher: UserOut = Depends(get_current_user), service = Depends(get_teacher_service)):
    new_teacher = ({"id": teacher.id, "FIO": FIO})
    return await service.create_teacher(new_teacher)

@router.get("/me",
            status_code=status.HTTP_200_OK,
            summary='Get current user as a teacher',)
async def get_current_user(user: UserOut = Depends(get_current_user),
                           service: TeacherService = Depends(get_teacher_service)):
    return await service.get(user.id)

@router.put("/me",
            status_code=status.HTTP_200_OK)
async def update_student(new_teacher: TeacherUpdateIn,
                        user: UserOut = Depends(get_current_user),
                         service: TeacherService = Depends(get_teacher_service)):
    return await service.update(new_teacher,user.id)



@router.get("/schedules/{week_number}&{FIO}",
             status_code=status.HTTP_200_OK,
             summary='Get schedule for teacher',
             description='Get schedule for any teacher.\n')
# добавить зависимость для зареганного юзера
async def get_schedule(week_number_schema: WeekNumber=Depends(get_week_number),  FIO_schema: FIO=Depends(get_FIO), service = Depends(get_teacher_service))->dict:
    return await service.get_schedule_by_FIO(FIO_schema.FIO, week_number_schema.week_number)



#в schedule
@router.get("/schedules/{week_number}",
             status_code=status.HTTP_200_OK,
             summary='Get my schedule',
             description='Get schedule for current teacher.\n')
async def get_schedule(week_number_schema: WeekNumber=Depends(get_week_number), teacher: UserOut = Depends(get_current_user), service = Depends(get_teacher_service))->dict:
    return await service.get_schedule(teacher.id, week_number_schema.week_number)



@router.get("/subjects_for_teacher/{FIO}",
             status_code=status.HTTP_200_OK,
             summary='Get subjects for any teacher',
             description='Get subjects for current teacher.\n')
async def get_subjects(FIO_schema: FIO=Depends(get_FIO), service = Depends(get_teacher_service))->list[str]:
    return await service.get_subjects_by_FIO(FIO_schema.FIO)

@router.get("/subjects",
             status_code=status.HTTP_200_OK,
             summary='Get my subjects',
             description='Get subjects for current teacher.\n')
async def get_subjects(teacher: UserOut = Depends(get_current_user), service = Depends(get_teacher_service))->list[str]:
    return await service.get_subjects(teacher.id)

@router.post("/subject",
             status_code=status.HTTP_201_CREATED,
             summary='Add new teacher subject',
             description='Add subject for current teacher.\n')
async def add_subject(subject: SubjectName, teacher: UserOut = Depends(get_current_user), service = Depends(get_teacher_service))->TeacherSubjectBase:
    return await service.add_subject(teacher.id, subject.name)

@router.delete("/subject",
             status_code=status.HTTP_200_OK,
             summary='Delete new teacher subject',
             description='Delete subject for current teacher.\n')
async def delete_subject(subject: SubjectName, teacher: UserOut = Depends(get_current_user), service = Depends(get_teacher_service))->TeacherSubjectBase:
    return await service.delete_subject(teacher.id, subject.name)


@router.delete("",
             status_code=status.HTTP_200_OK,
             summary='Delete teacher',
             description='Delete teacher. Requre FIO.\n')
async def delete(FIO: str, teacher: UserOut = Depends(get_current_user), service = Depends(get_teacher_service)):
    return await service.delete(FIO)



# РУЧКИ ДЛЯ АЧИВОК
# перенести в отдельную группу?

@router.post("/achievements/",
             status_code=status.HTTP_201_CREATED,
             summary='Create achievement',
             description='Create new achievement by teacher.\n',
             dependencies=[Depends(get_current_user)]
             )
async def create(achievement: AchieveIn,service = Depends(get_teacher_service)):
    return await service.create_achievement(achievement.name, achievement.description, achievement.amount)

@router.delete("/achievements/",
             status_code=status.HTTP_200_OK,
             summary='Delete achievement',
             description='Delete achievement for id.\n',
             dependencies=[Depends(get_current_user)]
              )
async def delete(achievement: AchieveID,service = Depends(get_teacher_service))->bool:
    return await service.delete_achievement(achievement.id)

@router.patch("/achievements/",
              status_code=status.HTTP_200_OK,
              summary='Update achievement',
              description='Update achievement.\n',
              dependencies=[Depends(get_current_user)]
              )
async def update(achievement: AchieveUpdate, service = Depends(get_teacher_service)):
    return await service.update_achievement(achievement.id, achievement.name, achievement.description, achievement.amount)


@router.post("/award_achievement",
             status_code=status.HTTP_200_OK,
             summary='Give achievement',
             description='Give achievement by student.\n',
             dependencies=[Depends(get_current_user)]
             )
async def give(student_id: int, achieve_id: int, service = Depends(get_teacher_service)):
    achieve = await service.give_achievement(student_id=student_id, achievement_id=achieve_id)
    return achieve


@router.delete("/revoke_achievement",
               status_code=status.HTTP_200_OK,
               summary='Revoke achievement',
               description='Revoke achievement from students\n',
               dependencies=[Depends(get_current_user)]
               )
async def give(student_id: int, achieve_id: int, service = Depends(get_teacher_service))->bool:
    return await service.revoke_achievement(student_id=student_id, achievement_id=achieve_id)


# Работа с лабами
@router.post("/lab_work",
             status_code=status.HTTP_201_CREATED,
             summary="Create lab work",
             description='Create new lab work\n',
             dependencies=[Depends(require_role(TEACHER_ROLE))]
             )
async def create(lab_work: LabWorkIn, teacher: UserOut = Depends(get_current_user),
                 service: TeacherService = Depends(get_teacher_service)):
    return await service.create_lab_work(lab_work.title, lab_work.description, lab_work.subject_name, teacher.id, lab_work.file_id)


@router.get("/lab_work/{lab_work_id}",
             status_code=status.HTTP_200_OK,
             summary="Get lab work",
             description='Get lab work by id\n',
             dependencies=[Depends(require_role(TEACHER_ROLE))]
             )
async def get(lab_work_schema: LabWorkID=Depends(get_lab_work_id), service: TeacherService = Depends(get_teacher_service)):
    return await service.get_lab_work(lab_work_schema.id)

@router.get("/lab_work",
             status_code=status.HTTP_200_OK,
             summary="Get all lab works",
             description='Create new lab work\n',
             dependencies=[Depends(require_role(TEACHER_ROLE))]
             )
async def get(service: TeacherService = Depends(get_teacher_service)):
    return await service.get_all_lab_work()

@router.post("/assignments",
             status_code=status.HTTP_201_CREATED,
             summary="Create assignment",
             description='Assign lab work to group\n',
             dependencies=[Depends(require_role(TEACHER_ROLE))]
             )
async def create(assignment: AssignmentsIn, teacher: UserOut = Depends(get_current_user),
                 service: TeacherService = Depends(get_teacher_service)):
    return await service.create_assignment(assignment.group_id, assignment.lab_id, teacher.id, assignment.created_at,
                                           assignment.deadline_at, assignment.status)

@router.get("/assignment/{assignment_id}",
             status_code=status.HTTP_200_OK,
             summary="Get assignment",
             description='Get assigned lab\n',
             dependencies=[Depends(require_role(TEACHER_ROLE))]
             )
async def get(assignment_schema: AssignmentID=Depends(get_lab_work_id), service: TeacherService = Depends(get_teacher_service)):
    return await service.get_assignment(assignment_schema.id)


@router.get("/assignment",
             status_code=status.HTTP_200_OK,
             summary="Get assignment",
             description='Get assigned lab\n',
             dependencies=[Depends(require_role(TEACHER_ROLE))]
             )
async def get(service: TeacherService = Depends(get_teacher_service)):
    return await service.get_all_assignment()


