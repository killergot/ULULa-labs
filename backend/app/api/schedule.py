from datetime import datetime, timedelta

from fastapi import Depends, HTTPException,status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.requests import Request
from uuid import UUID, uuid4
from database.models.schedule import Schedule
from database.psql import get_db
from crud.schedule import ScheduleService

router = APIRouter(prefix="/schedule", tags=["schedule"])

@router.post("/add_schadule", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_chedule(group_number: str, week_number: int,
                        monday: dict | None = None,
                        tuesday: dict | None = None,
                        wednesday: dict | None = None,
                        thursday: dict | None = None,
                        friday: dict | None = None,
                        saturday: dict | None = None,
                        sunday: dict | None = None,
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




@router.patch("/update_schadule", response_model=None, status_code=status.HTTP_201_CREATED)
async def update_schedule(group_number: str, week_number: int,
                        monday: dict | None = None,
                        tuesday: dict | None = None,
                        wednesday: dict | None = None,
                        thursday: dict | None = None,
                        friday: dict | None = None,
                        saturday: dict | None = None,
                        sunday: dict | None = None,
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