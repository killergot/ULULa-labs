from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from app.repositoryes.shared_links_repository import SharedLinkRepository
from app.repositoryes.user_repository import UserRepository
from app.repositoryes.task_repository import Repository as TaskRepository
from app.shemas.tasks import SharedLinkIn
from fastapi import  HTTPException, status

class SharedLinkService:
    def __init__(self, db: AsyncSession):
        self.repo = SharedLinkRepository(db)
        self.user_repo = UserRepository(db)
        self.tasks_repo = TaskRepository(db)

    async def create(self, new_link: SharedLinkIn): #создаём новую группу
        if not await self.user_repo.get_by_id(new_link.user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User {new_link.user_id} does not exist")
        if not await self.tasks_repo.get_by_id(new_link.task_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Task {new_link.task_id} does not exist")

        if new_link.expires_at and new_link.expires_at < datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Expiration date {new_link.expires_at} invalid")

        new_link = await self.repo.create(new_link.task_id,
                                          new_link.user_id,
                                          new_link.expires_at)
        return new_link

    async def get(self,id: int, user_id: int):
        link = await self.repo.get(id)
        if not link or link.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"SharedLink {id} not found")
        return link

    async def get_by_token(self,token: UUID):
        link = await self.repo.get_by_token(token)
        if not link:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"SharedLink {token} not found")
        return link

    async def get_all(self, user_id: int):
        links = await self.repo.get_all(user_id)
        return links

    async def delete(self, id: int,user_id: int):
        link = await self.repo.get(id)
        if not link or link.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"SharedLink {id} not found")
        if not await self.repo.delete(link):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"SharedLink {id} not found")
