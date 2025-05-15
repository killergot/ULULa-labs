import logging
from sqlalchemy import select
from uuid import UUID
from app.database.models.teachers import Teacher
from app.database.models.groups import Group
from app.repositoryes.template import TemplateRepository
from app.core.except_handler import except_handler

log = logging.getLogger(__name__)

class Repository(TemplateRepository):
    async def get_all(self):
        data = select(Teacher)
        teachers= await self.db.execute(data)
        return teachers.scalars().all()


    async def get_by_id(self, id: int)->Teacher:
            print ("hello")
            data = select(Teacher).where (Teacher.id == id)
            student = await self.db.execute(data)
            return  student.scalars().first()

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
        print("hello 1")
        teacher = await self.get_by_id(id)
        print (teacher.FIO)
        await self.db.delete(teacher)
        await self.db.commit()
        return True

    @except_handler
    async def update(self, student_id: int, group_id: str):
        student = await self.get_by_id(student_id)
        student.group_id = group_id
        await self.db.commit()
        await self.db.refresh(student)
        return student