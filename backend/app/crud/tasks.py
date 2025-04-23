from datetime import datetime, timedelta
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Date
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from app.database.models.tasks import Task
from app.services.jwt import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.services.oauth import oauth
from app.shemas.auth import UserCreate
from hashlib import sha256


class TaskService:

    @classmethod
    def read_task(cls,db: Session, id: int):
        # Создание задачи
            task = db.query(Task).filter(Task.task_id==id).first()
            if not task:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task not exist"
            )
            return 
    
    @classmethod
    def get_all(cls,db: Session):
        tasks = db.query(Task).all()
        return tasks

    @classmethod
    def create_task(cls,db: Session, id: UUID, deadline: Date,  description: str):
        # Создание задачи
            db_task = Task(user_id=id, deadline=deadline, description=description)
            try:
                db.add(db_task)
                db.commit()
                db.refresh(db_task)
            except Exception as e:
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=str(e)
                )

            return db_task
    
    @classmethod
    def delete_task(cls,db: Session, id: int):
            task = db.query(Task).filter(Task.task_id==id).first()
            if not task:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task not exist"
            )
            try:
                db.delete(task)
                db.commit()
                return {"Result:" "Success delete"}
            except Exception as e:
                db.rollback()
                raise e
    

    @classmethod
    def update_task(cls,db: Session, id: int, deadline: Date,  description: str):
        existing_task = db.query(Task).filter(Task.task_id == id).first()
        db_task = Task(task_id=id)
        if existing_task:
            # Студент с таким ID уже существует, обновляем group_number
            existing_task.deadline = deadline
            existing_task.description= description
            try:
                db.commit()  # Commit without add() when updating
                db.refresh(existing_task)
                return existing_task
            except Exception as e:
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=str(e)
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task not registered yet"
            )