import logging
from datetime import datetime
from typing import Optional

from sqlalchemy import select, text
from app.database.models.shared_links import SharedLink
from uuid import UUID
from app.database.models.groups import Group
from app.repositoryes.template import TemplateRepository
from app.core.except_handler import except_handler
from app.shemas.schedule import ScheduleIn, ScheduleBase
from sqlalchemy.orm import selectinload


log = logging.getLogger(__name__)


class SharedLinkRepository(TemplateRepository):
    async def create(self, task_id: int, user_id: int, expire_at: Optional[datetime] = None):
        link = SharedLink(
            task_id = task_id,
            user_id = user_id,
        )
        if expire_at:
            link.expires_at = expire_at
        self.db.add(link)
        await self.db.commit()
        await self.db.refresh(link)
        return link

    async def get(self, id: int):
        data = select(SharedLink).where(SharedLink.id == id).options(
            selectinload(SharedLink.task)
        )
        subject = await self.db.execute(data)
        return subject.scalars().first()

    async def get_by_token(self, token):
        data = select(SharedLink).where(SharedLink.token == token).options(
            selectinload(SharedLink.task)
        )
        subject = await self.db.execute(data)
        return subject.scalars().first()

    async def get_all(self, user_id: int):
        data = select(SharedLink).where(SharedLink.user_id == user_id)
        subject = await self.db.execute(data)
        return subject.scalars().all()

    async def delete(self, link: SharedLink):
        await self.db.delete(link)
        await self.db.commit()
        return True

