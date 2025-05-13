import logging
from sqlalchemy import select, text, insert
from sqlalchemy.dialects.postgresql import insert as pg_insert
from uuid import UUID
from app.database.models.teacher_subjects import TeacherSubject
from app.database.models.groups import Group
from app.repositoryes.template import TemplateRepository
from app.core.except_handler import except_handler
from app.shemas.schedule import ScheduleIn, ScheduleBase

log = logging.getLogger(__name__)


class Repository(TemplateRepository):

    async def clean(self):
        await self.db.commit()
        await self.db.execute(text("TRUNCATE TABLE teacher_subjects RESTART IDENTITY CASCADE"))
        await self.db.commit()

    async def create_by_list(self, teacher_subjects):


        stmt = pg_insert(TeacherSubject.__table__).values(teacher_subjects)
        stmt = stmt.on_conflict_do_nothing(index_elements=["teacher_id", "subject_id"])
        await self.db.execute(stmt)
        await self.db.commit()

    async def get(self, id: int)->list[TeacherSubject]:
        stmt = \
            (select(TeacherSubject)
            .where(TeacherSubject.teacher_id == id)
        )
        result = await self.db.execute(stmt)
        subjects = result.scalars().all()
        return subjects


    async def is_exist(self, teacher_id: int, subject_id: int) -> TeacherSubject:
        stmt = \
            (select(TeacherSubject)
             .where(TeacherSubject.teacher_id == teacher_id, TeacherSubject.subject_id == subject_id )
             )
        result = await self.db.execute(stmt)
        subject = result.scalars().first()
        return subject

    async def create(self, teacher_id: int, subject_id: int) -> TeacherSubject:
        new = TeacherSubject(teacher_id = teacher_id, subject_id =  subject_id)
        self.db.add(new)
        await self.db.commit()
        return new

    async def delete(self, teacher_id: int, subject_id: int) -> TeacherSubject:
        new = await  self.is_exist(teacher_id = teacher_id, subject_id =  subject_id)
        #print(new.subject_id, new.teacher_id)
        await self.db.delete(new)
        await self.db.commit()
        return new
