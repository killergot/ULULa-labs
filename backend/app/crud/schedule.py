from datetime import datetime, timedelta
from sqlalchemy.dialects.postgresql import UUID
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from app.database.models.schedule import Schedule
from app.services.jwt import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.services.oauth import oauth
from app.shemas.auth import UserCreate
from hashlib import sha256
from typing import Optional

class ScheduleService:
    @classmethod
    def is_schedule_exist(cls,db: Session, group_number: str, week_number: int):
        return db.query(Schedule).filter(Schedule.group_number == group_number, Schedule.week_number == week_number).first()

    @classmethod
    def create_schedule(cls,db: Session, group_number: str, week_number: int,
                        monday: Optional[dict] = None,
                        tuesday: Optional[dict] = None,
                        wednesday: Optional[dict] = None,
                        thursday: Optional[dict] = None,
                        friday: Optional[dict] = None,
                        saturday: Optional[dict] = None,
                        sunday: Optional[dict] = None):
        if cls.is_schedule_exist(db, group_number, week_number):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Schedule already registered"
            )
        db_schedule = Schedule(group_number=group_number,  week_number=week_number, monday=monday, tuesday=tuesday,
                               wednesday=wednesday,
                               thursday=thursday,
                               friday=friday,
                               saturday=saturday,
                               sunday=sunday)
        
        try:
                db.add(db_schedule)
                db.commit()
                db.refresh(db_schedule)
                db.commit()
        except Exception as e:
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=str(e)
                )

        return db_schedule
                       
    @classmethod
    #добавить логику изменения при отсутствующих параметрах???
    def update_schedule(cls,db: Session, group_number: str, week_number: int,
                        monday: Optional[dict] = None,
                        tuesday: Optional[dict] = None,
                        wednesday: Optional[dict] = None,
                        thursday: Optional[dict] = None,
                        friday: Optional[dict] = None,
                        saturday: Optional[dict] = None,
                        sunday: Optional[dict] = None):
        existing_schedule = cls.is_schedule_exist(db, group_number, week_number)
        if existing_schedule:
            existing_schedule.monday=monday
            existing_schedule.teuesday=tuesday
            existing_schedule.thursday=thursday
            existing_schedule.wednesday=wednesday
            existing_schedule.thursday=thursday
            existing_schedule.friday=friday
            existing_schedule.saturday=saturday
            existing_schedule.sunday=sunday
            try:
                db.commit()  # Commit without add() when updating
                db.refresh(existing_schedule)
                return existing_schedule
            except Exception as e:
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=str(e)
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Schedule not registered yet"
            )