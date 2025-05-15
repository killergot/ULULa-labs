import os

from fastapi import  HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositoryes.group_items_repository import GroupItemsRepository

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class GroupFilesService:
    def __init__(self, db: AsyncSession):
        self.repo = GroupItemsRepository(db)

    async def _get(self, id: int):
        file = await self.repo.get(id)
        if not file:
            raise HTTPException(status_code=404,
                                detail=f"File with id {id} not found")
        return file

    async def get(self, id: int):
        file = await self._get(id)
        return file

    async def get_filtered(self, ):
