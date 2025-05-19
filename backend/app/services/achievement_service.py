from fastapi import  HTTPException, status
from typing import Optional

from app.repositoryes.achievements_repository import AchivementRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositoryes.achievements_repository import AchivementRepository
from app.database.models.achievent import Achievement


class AchievementService:
    def __init__(self, db: AsyncSession):
        self.repo = AchivementRepository(db)


    async def get_filtered(self, name: str, description: str, amount: int) -> list[Achievement]:
        return await self.repo.get_filtered(name, description, amount)

    async def get_achievement(self, id):
        achievement = await self.repo.get(id)
        if not achievement:
            raise HTTPException(status_code=404,
                                detail="Achievement not found")
        return achievement