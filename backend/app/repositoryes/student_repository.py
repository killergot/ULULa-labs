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
        data = select(Student.group_id, Student.id)
        student = await self.db.execute(data)
        return [{"group_id": row.group_id, "id": row.id} for row in student]


    async def get_by_group(self, id: int):
            data = select(Student.id).where (Student.group_id == id)
            student = await self.db.execute(data)
            return  student.scalars().all()

    async def create(self, student_id: int,
                     group_id: int) -> Student:
        new_student = Student(
            id = student_id, group_id = group_id
        )
        self.db.add(new_student)
        await self.db.commit()
        await self.db.refresh(new_student)
        return {'student_id': new_student.id, 'group_id': new_student.group_id}

    async def get_by_id(self, id: int):
        return await self.db.get(Student, id)

    @except_handler
    async def delete(self, student_id: int) -> bool:
        await self.db.delete(await self.get_by_id(student_id))
        await self.db.commit()
        return True

    @except_handler
    async def update(self, student_id: int, group_id: str):
        student = await self.get_by_id(student_id)
        student.group_id = group_id
        await self.db.commit()
        await self.db.refresh(student)
        return student