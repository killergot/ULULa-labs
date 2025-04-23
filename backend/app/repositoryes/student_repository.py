from typing import Optional
import logging

from sqlalchemy import select

from uuid import UUID
from app.database.models.students import Student
from app.database.models.groups import Group
from app.repositoryes.template import TemplateRepository
from app.core.except_handler import except_handler

log = logging.getLogger(__name__)

class Repository(TemplateRepository):
    async def get_all(self):
        data = select(Group)
        student = await self.db.execute(data)
        return student.scalars().all()

    async def get_group(self, id: int):# Получаем id группы по id студента. Можем использовать для проверки существования
        data = select(Student).where(Student.group_id == id)
        student = await self.db.execute(data)
        return student.scalars().first()

    async def create(self, student_id: int,
                     group_id: int) -> Student:
        new_student = Student(
            student_id, group_id
        )
        self.db.add(new_student)
        await self.db.commit()
        await self.db.refresh(new_student)
        return new_student


    async def get_by_id(self, user_id: int):
        return await self.db.get(User, user_id)



    @except_handler
    async def update(self, user_id: int, password: str):
        user = await self.get_by_id(user_id)
        user.password = password
        await self.db.commit()
        await self.db.refresh(user)
        return user

    @except_handler
    async def delete(self, user_id: int) -> bool:
        await self.db.delete(await self.get_by_id(user_id))
        await self.db.commit()
        return True