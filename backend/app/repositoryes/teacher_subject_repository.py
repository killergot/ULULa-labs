import logging
from sqlalchemy import select, text
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

