import logging
from sqlalchemy import select, text
from sqlalchemy.dialects.postgresql import insert as pg_insert
from uuid import UUID
from app.database.models.group_subjects import GroupSubject
from app.database.models.groups import Group
from app.repositoryes.template import TemplateRepository
from app.core.except_handler import except_handler
from app.shemas.schedule import ScheduleIn, ScheduleBase

log = logging.getLogger(__name__)


class Repository(TemplateRepository):

    async def clean(self):
        await self.db.commit()
        await self.db.execute(text("TRUNCATE TABLE group_subjects RESTART IDENTITY CASCADE"))
        await self.db.commit()

    async def create_by_list(self, group_subjects):
        batch_size = 1000
        for i in range(0, len(group_subjects), batch_size):
            batch = group_subjects[i:i + batch_size]
            stmt = pg_insert(GroupSubject.__table__).values(batch)
            stmt = stmt.on_conflict_do_nothing(index_elements=["group_id", "subject_id"])
            await self.db.execute(stmt)
            await self.db.commit()

