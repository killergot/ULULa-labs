from datetime import datetime, timedelta
from sqlalchemy.dialects.postgresql import UUID
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from app.database.models.students import Student

from hashlib import sha256

class StudentService:
    @classmethod
    def is_student_exist(cls,db: Session, id: UUID):
                student =  db.query(Student).filter(Student.id == id).first()
                return student

    @classmethod
    def read_groups(cls, db:Session):
        group = db.query(Student.group_number).all()
        return group

    @classmethod
    def create_student(cls,db: Session, id: UUID, group_number: str):
        # Создание объекта пользователя
        existing_student = db.query(Student).filter(Student.id == id).first()
        if existing_student:
            # Студент с таким ID уже существует, обновляем group_number
            existing_student.group_number = group_number
            try:
                db.commit()  # Commit without add() when updating
                db.refresh(existing_student)
                return existing_student
            except Exception as e:
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=str(e)
                )
        else:
            db_student = Student(id=id, group_number=group_number)

            try:
                db.add(db_student)
                db.commit()
                db.refresh(db_student)
            except Exception as e:
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=str(e)
                )

            return db_student


    @classmethod
    def read_student(cls,db: Session, id: UUID, group_number: str):
        # Создание объекта пользователя
        existing_student = db.query(Student).filter(Student.id == id).first()
        if existing_student:
            # Студент с таким ID уже существует, обновляем group_number
            return existing_student
        else:
            return {"Result:": "student not found"}



    @classmethod
    def delete_student(cls,db: Session, id: UUID):
        # Создание объекта пользователя
        existing_student = db.query(Student).filter(Student.id == id).first()
        if existing_student:
            try:
                db.delete(existing_student)
                db.commit()
                return {"Result:" "Success delete"}
            except Exception as e:
                db.rollback()
                raise e
        else:
            return {"Result:": "Student not found"}