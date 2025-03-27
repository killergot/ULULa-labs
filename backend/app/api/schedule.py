from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException,status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.requests import Request
from uuid import UUID, uuid4
from app.database.models.schedule import Schedule
from app.database.psql import get_db
from app.crud.schedule import ScheduleService

router = APIRouter(prefix="/schedule", tags=["schedule"])

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