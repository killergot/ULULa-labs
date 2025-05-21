from typing import Optional
import logging

from sqlalchemy import select

from uuid import UUID

from sqlalchemy.orm import selectinload

from app.database.models.auth import User, UserSession
from app.database.models.groups import Group
from app.repositoryes.template import TemplateRepository
from app.core.except_handler import except_handler

log = logging.getLogger(__name__)

class UserRepository(TemplateRepository):
    async def get_all(self):
        data = select(User)
        users = await self.db.execute(data)
        return users.scalars().all()

    async def get_with_sessions(self,user_id:int):
        data = (select(User).
        where(User.id == user_id).
        options(
                selectinload(User.sessions)
            ))
        users = await self.db.execute(data)
        user = users.scalars().first()
        return user

    async def get_by_email(self, email: str):
        data = select(User).where(User.email == email)
        user = await self.db.execute(data)
        return user.scalars().first()

    async def get_by_id(self, user_id: int):
        return await self.db.get(User, user_id)

    async def create(self,email: str,
                     password: Optional[str] = None,
                     role: int = 0,
                     auth_provider: Optional[str] = None,
                     provider_id: Optional[str] = None) -> User:
        new_user = User(email=email,
                        password=password,
                        role=role,
                        auth_provider=auth_provider,
                        provider_id=provider_id)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user

    @except_handler
    async def update(self, user: User, password: str):
        user.password = password
        await self.db.commit()
        await self.db.refresh(user)
        return user


    @except_handler
    async def delete(self, user_id: int) -> bool:
        await self.db.delete(await self.get_by_id(user_id))
        await self.db.commit()
        return True