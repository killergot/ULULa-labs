import logging
from sqlalchemy import select, text
from sqlalchemy.dialects.postgresql import insert as pg_insert
from uuid import UUID
from app.database.models.subjects import Subject
from app.database.models.groups import Group
from app.repositoryes.template import TemplateRepository
from app.core.except_handler import except_handler
from app.shemas.schedule import ScheduleIn, ScheduleBase

log = logging.getLogger(__name__)


class Repository(TemplateRepository):

    async def clean(self):
        await self.db.commit()
        await self.db.execute(text("TRUNCATE TABLE subjects RESTART IDENTITY CASCADE"))
        await self.db.commit()

    async def create_by_list(self, subjects):
        stmt = pg_insert(Subject.__table__).values(subjects)
        stmt = stmt.on_conflict_do_nothing(index_elements=["name"])
        await self.db.execute(stmt)
        await self.db.commit()

    async def get_by_name(self, name: str):
        return await self.db.get(Subject, name)


