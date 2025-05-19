import logging
from typing import Optional

from sqlalchemy import select
from uuid import UUID

from sqlalchemy.orm import selectinload

from app.database.models.teachers import Teacher
from app.database.models.groups import Group
from app.repositoryes.template import TemplateRepository
from app.core.except_handler import except_handler
from app.shemas.teachers import TeacherUpdateIn

log = logging.getLogger(__name__)

class Repository(TemplateRepository):
    async def get_all(self):
        data = select(Teacher)
        teachers= await self.db.execute(data)
        return teachers.scalars().all()


    async def get_by_id(self, id: int)->Teacher:
        data = select(Teacher).where (Teacher.id == id)
        student = await self.db.execute(data)
        return  student.scalars().first()

    async def get(self, id: int)->Teacher:
        data = (select(Teacher).where(Teacher.id == id)
        .options(
            selectinload(Teacher.user)
        ))
        teacher = await self.db.execute(data)
        return teacher.scalars().first()

    async def create(self, id, FIO)->Teacher:
        new_teacher = Teacher(
            id = id, FIO = FIO
        )
        self.db.add(new_teacher)
        await self.db.commit()
        await self.db.refresh(new_teacher)
        return {'teacher_id': new_teacher.id, 'FIO': new_teacher.FIO}

    async def get_by_FIO(self, FIO: str) -> Teacher:
        data = select(Teacher).where(Teacher.FIO == FIO)
        teacher = await self.db.execute(data)
        return teacher.scalars().first()

    @except_handler
    async def delete(self, id: int) -> bool:
        teacher = await self.get_by_id(id)
        await self.db.delete(teacher)
        await self.db.commit()
        return True

    @except_handler
    async def update(self, student: Teacher,
                     FIO: Optional[str] = None,
                     telegram: Optional[str] = None,
                     avatar: Optional[str] = None,
                     nickname: Optional[str] = None,
                     email: Optional[str] = None,):
        if FIO is not None:
            student.FIO = FIO
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