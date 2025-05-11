
#from app.utils.get_schedule import load_schedule_for_all_groups
from fastapi.openapi.utils import get_openapi_operation_metadata
from fastapi.routing import APIRouter
from fastapi import Depends, status
from app.shemas.groups import GroupBase, GroupID, GroupNumber
from app.api.depencies.guard import get_current_user, require_role
from app.api.depencies.services import get_schedule_service, get_group_service, get_student_service
from app.shemas.schedule import ScheduleIn, ScheduleBase, ScheduleGetIn
from app.shemas.groups import GroupID, GroupNumber
from app.shemas.students import StudentBase, StudentIn, StudentID
from app.shemas.auth import UserOut
from app.utils.get_schedule import get_groups
from app.api.depencies.services import get_group_service
router = APIRouter(prefix="/schedule", tags=["schedule"])

# Что хотим уметь для сущности расписания?
# 1.1 ++ Добавлять/изменять расписание по id группы и номеру недели вручную (если группы нет - создаём по умолчанию)
# 1.2 ++ Добавлять/изменя расписание по номеру группы и номеру недели (если группы нет - создаём по умолчанию)
# 2.1 Загружать расписание целиком с сайта
# 2.2 Загружать расписание для конкретной группы с сайта по номеру группы (сразу на 4 недели?)
# 2.3 Загружать расписание для конкретной группы с сайта по id группы

#Нужно ли удаление? Как будто только при удалении самой группы

# 3.1 ++ Удаление расписания по номеру группы на все недели
# 3.2 ++ Удаление расписания по id группы на все недели
# 4.1 ++ Получать все расписания
# 4.2 ++ Получать расписание по номеру группы и номеру недели
# 4.3 ++ Получать расписание по id группы и номеру недели
# 4.4 ++ Получать расписание по номеру студента и номеру недели
# 4.5 ++ Получать расписание для текущего студента и номеру недели



@router.post("/load_schedule")
async def load_schedule(service = Depends(get_schedule_service), group_service = Depends(get_group_service)):
    # Получать группы по одной из списка
    await service.load_schedule()
    return {"Result": "schedule was successfully load"}



@router.post("/change_schedule_by_number",
             status_code=status.HTTP_201_CREATED,
             summary='Change_schedule',
             description='Change existing schedule (For all groups schedule already exist)\n',
             #dependencies=[Depends(get_current_user)] #заменить на закомментированную строку, чтобы работало только от админа
             #dependencies=[Depends(require_role(1))
)
async def create_schedule(schedule: ScheduleIn,  service = Depends(get_schedule_service), group_service = Depends(get_group_service)):
    # group_id = преобразовать нормер в id
    group_id = await  group_service.get_by_number(GroupNumber.model_validate({"group_number": schedule.group_number}))
    print (type(schedule.monday))
    new_schedule = ScheduleBase.model_validate({"group_id": group_id, "week_number": schedule.week_number,
                                                "monday": schedule.monday,
                                                "tuesday":  [],
                                                "wednesday": [],
                                                "thursday":  [],
                                                "friday":  [],
                                                "saturday":  [],
                                                "sunday":  []
                                                })
    return await service.create_schedule(new_schedule)


@router.post("/change_schedule_by_id",
             status_code=status.HTTP_201_CREATED,
             summary='Change_schedule',
             description='Change existing schedule (For all groups schedule already exist)\n',
             #dependencies=[Depends(get_current_user)] #заменить на закомментированную строку, чтобы работало только от админа
             #dependencies=[Depends(require_role(1))
)
async def create_schedule(schedule: ScheduleBase,  service = Depends(get_schedule_service)):
    return await service.create_schedule(schedule)



@router.delete("/delete_schedule_by_id",
             status_code=status.HTTP_200_OK,
             summary='Delete schedule',
             description='Delete schedule by group number.\n',
             dependencies=[Depends(get_current_user)] #заменить на закомментированную строку, чтобы работало только от админа
             #dependencies=[Depends(require_role(1))
)
async def delete_schedule(group_id: int, service = Depends(get_schedule_service)):
    return await service.delete_schedule(group_id)


@router.delete("/delete_schedule_by_number",
             status_code=status.HTTP_200_OK,
             summary='Delete schedule',
             description='Delete schedule by group number.\n',
             dependencies=[Depends(get_current_user)] #заменить на закомментированную строку, чтобы работало только от админа
             #dependencies=[Depends(require_role(1))
)
async def delete_schedule(group_number: str, service = Depends(get_schedule_service), group_service = Depends(get_group_service)):
    group_id = await  group_service.get_by_number(GroupNumber.model_validate({"group_number": group_number}))
    return await service.delete_schedule(group_id)



@router.get("/get_all",
             status_code=status.HTTP_200_OK,
             summary='Get all schedule',
             description='Get all schedule.\n',
             dependencies=[Depends(get_current_user)] #заменить на закомментированную строку, чтобы работало только от админа
             #dependencies=[Depends(require_role(1))
)
async def get_all(service = Depends(get_schedule_service)):
       return await service.get_all()



@router.get("/get_by_id/{group_id, week_number}",
             status_code=status.HTTP_200_OK,
             summary='Get schedule by group id',
             description='Get schedule.\n',
             dependencies=[Depends(get_current_user)] #заменить на закомментированную строку, чтобы работало только от админа
             #dependencies=[Depends(require_role(1))
)
async def get_schedule(group_id: int, week_number: int, service = Depends(get_schedule_service)):
        group_week = ScheduleGetIn.model_validate({"group_id": group_id, "week_number": week_number})
        return await service.get_by_id(group_week.group_id, group_week.week_number)


@router.get("/get_by_number/{group_number, week_number}",
             status_code=status.HTTP_200_OK,
             summary='Get schedule by group number',
             description='Get schedule by number.\n',
             dependencies=[Depends(get_current_user)] #заменить на закомментированную строку, чтобы работало только от админа
             #dependencies=[Depends(require_role(1))
)
async def get_schedule(group_number: str, week_number: int, service = Depends(get_schedule_service),  group_service = Depends(get_group_service)):
        group_id = await  group_service.get_by_number(GroupNumber.model_validate({"group_number": group_number}))
        group_week = ScheduleGetIn.model_validate({"group_id": group_id, "week_number": week_number})
        return await service.get_by_id(group_week.group_id, group_week.week_number)


@router.get("/get_by_student/{student_number, week_number}",
             status_code=status.HTTP_200_OK,
             summary='Get schedule by student number',
             description='Get schedule by student number.\n',
             dependencies=[Depends(get_current_user)] #заменить на закомментированную строку, чтобы работало только от админа
             #dependencies=[Depends(require_role(1))
)
async def get_schedule(student_number: int, week_number: int, service = Depends(get_schedule_service),  student_service = Depends(get_student_service)):
        group_id = await  student_service.get_group(StudentID.model_validate({"student_id": student_number}).student_id)
        group_week = ScheduleGetIn.model_validate({"group_id": group_id, "week_number": week_number})
        return await service.get_by_id(group_week.group_id, group_week.week_number)


@router.get("/get_for_current_student/{week_number}",
             status_code=status.HTTP_200_OK,
             summary='Get schedule for current user',
             description='Get schedule for current user.\n',
)
async def get_schedule(week_number: int, student: UserOut = Depends(get_current_user), service = Depends(get_schedule_service),  student_service = Depends(get_student_service)):

        group_id = await  student_service.get_group(student.id)
        group_week = ScheduleGetIn.model_validate({"group_id": group_id, "week_number": week_number})
        return await service.get_by_id(group_week.group_id, group_week.week_number)
'''
@router.get("/load_schedule")
async def load_schedule():
    try:
        load_all_schedule()
    except Exception as e:
        return {"Error when load schedule: ", e}
    return {"Result": "schedule was successfully load"}


@router.post("/add_schadule", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_student(group_number: str, week_number: int,
                        monday: Optional[dict] = None,
                        tuesday: Optional[dict] = None,
                        wednesday: Optional[dict] = None,
                        thursday: Optional[dict] = None,
                        friday: Optional[dict] = None,
                        saturday: Optional[dict] = None,
                        sunday: Optional[dict] = None,
                        db: Session = Depends(get_db)) -> dict[str, any]:
    try:
        schedule = ScheduleService.create_schedule(db, group_number, week_number, monday, tuesday, wednesday, thursday, friday, saturday, sunday)
        # Создаем словарь для возврата данных
        response_data = {
            "group_number": schedule.group_number,
            "week_number": schedule.week_number,
            "monday": monday,
            "tuesday": tuesday,
            "wednesday": wednesday,
            "thursday": thursday,
            "friday": friday,
            "saturday": saturday,
            "sunday": sunday
        }
        return response_data
    except HTTPException as e:
        raise e  # Пробрасываем HTTPException дальше
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    

@router.get("/read_schedule")
async def read_schedule(group_number: str, week_number: int, db: Session = Depends(get_db)):
    try:
        schedule = ScheduleService.is_schedule_exist(db, group_number, week_number)
    except HTTPException as e:
        raise HTTPException(status_code=404, detail="Schedule not found")
    if schedule: 
        response_data = {
        "group_number": schedule.group_number,
        "week_number": schedule.week_number,
        "monday": schedule.monday,
        "tuesday": schedule.tuesday,
        "wednesday": schedule.wednesday,
        "thursday": schedule.thursday,
        "friday": schedule.friday,
        "saturday": schedule.saturday,
        "sunday": schedule.sunday
            }
    else: 
        response_data = {
            "Result: this schedule not exist(("
        }
    return response_data


@router.post("/update_schadule", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_student(group_number: str, week_number: int,
                        monday: Optional[dict] = None,
                        tuesday: Optional[dict] = None,
                        wednesday: Optional[dict] = None,
                        thursday: Optional[dict] = None,
                        friday: Optional[dict] = None,
                        saturday: Optional[dict] = None,
                        sunday: Optional[dict] = None,
                        db: Session = Depends(get_db)) -> dict[str, any]:
    try:
        schedule = ScheduleService.update_schedule(db, group_number, week_number, monday, tuesday, wednesday, thursday, friday, saturday, sunday)
        # Создаем словарь для возврата данных
        response_data = {
            "group_number": schedule.group_number,
            "week_number": schedule.week_number,
            "monday": monday,
            "tuesday": tuesday,
            "wednesday": wednesday,
            "thursday": thursday,
            "friday": friday,
            "saturday": saturday,
            "sunday": sunday
        }
        return response_data
    except HTTPException as e:
        raise e  # Пробрасываем HTTPException дальше
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )



@router.delete("/del_schedule")
async def delete_schedule(group_number: str, week_number: int, db: Session = Depends(get_db)):
    try:
        ScheduleService.delete_schedule(db, group_number, week_number)
    except HTTPException as e:
        raise HTTPException(status_code=404, detail= "Schedule not found")
    return {"message": "Schedule deleted successfully"}
'''