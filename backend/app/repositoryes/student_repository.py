import logging
from math import trunc
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID
from app.database.models.students import Student
from app.database.models.groups import Group
from app.database.models.subjects import Subject
from app.repositoryes.template import TemplateRepository
from app.core.except_handler import except_handler

log = logging.getLogger(__name__)

class Repository(TemplateRepository):
    async def get_all(self):
        data = select(Student.group_id, Student.id)
        student = await self.db.execute(data)
        return [{"group_id": row.group_id, "id": row.id} for row in student]


    async def get_by_group(self, id: int):
            data = select(Student.id).where(Student.group_id == id)
            student = await self.db.execute(data)
            return  student.scalars().all()

    async def create(self, student_id: int,
                     group_id: int,
                     full_name: str) -> Student:
        new_student = Student(
            id = student_id, group_id = group_id, full_name = full_name
        )
        self.db.add(new_student)
        await self.db.commit()
        await self.db.refresh(new_student)
        return new_student

    async def get(self, student_id: int):
        stmt = (
            select(Student)
            .where(Student.id == student_id)
            .options(
                selectinload(Student.achievements),  # Явно загружаем achievements
                selectinload(Student.user),  # И пользователя, если нужно
                selectinload(Student.group),  # И группу
                selectinload(Student.subjects)
            )
        )
        result = await self.db.execute(stmt)
        student = result.scalars().first()
        return student

    @except_handler
    async def delete(self, student_id: int) -> bool:
        await self.db.delete(await self.get(student_id))
        await self.db.commit()
        return True

    @except_handler
    async def update(self, student: Student,
                     group_id: Optional[Group] = None,
                     full_name: Optional[str] = None,
                     telegram: Optional[str] = None,
                     avatar: Optional[str] = None,
                     nickname: Optional[str] = None,
                     email: Optional[str] = None,):
        if group_id is not None:
            student.group_id = group_id
        if full_name is not None:
            student.full_name = full_name
        if telegram is not None:
            student.telegram = telegram
        if avatar is not None:
            student.avatar_url = avatar
        if nickname is not None:
            student.nickname = nickname
        if email is not None:
            student.user.email = email

        await self.db.commit()
        await self.db.refresh(student)
        return student

    async def add_subject(self,student: Student, subject: Subject):
        student.subjects.append(subject)
        await self.db.commit()
        await self.db.refresh(student)
        return student

    async def delete_subject(self, student,subject):
        student.subjects.remove(subject)
        await self.db.commit()
        await self.db.refresh(student)
        return True