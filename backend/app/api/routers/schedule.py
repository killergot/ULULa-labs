from datetime import datetime, timedelta

from fastapi import Depends, HTTPException,status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.models.schedule import Schedule
from app.database.psql import get_db
from app.crud.schedule import ScheduleService
from app.services.get_schedule import load_schedule_for_group, load_all_schedule
from starlette.requests import Request
from uuid import UUID, uuid4

from typing_extensions import Optional

from app.database.models.schedule import Schedule
from app.database.psql import get_db
from app.crud.schedule import ScheduleService

router = APIRouter(prefix="/schedule", tags=["schedule"])

# Что хотим уметь для сущности расписания?
# 1 - Добавлять/изменять расписание по (номеру или id???) группы "вручную" (вход - полное или неполное расписание, номер/id группы, номер недели, выход - успех/неуспех)
# 2.1 - Удалять расписание (вход - номер/id группы, номер недели, выход - успех/неуспех)
# 2.2 - Удалять расписание для всех недель (вход - номер/id группы, номер недели, выход - успех/неуспех)
# 3.1 - Загружать расписание с сайта группе
# 3.2 - Загружать расписание для всех групп
# 4 - Получать расписание для конкретной группы (вход - номер группы, )
# 5 - Получать расписание для пользователя (по id пользователя)

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