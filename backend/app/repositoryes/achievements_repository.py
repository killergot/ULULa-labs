from wtforms.validators import Optional

from app.database.models.achievent import Achievement
from app.database.models.students import Student
from app.repositoryes.template import TemplateRepository
from sqlalchemy import select, and_
from typing import Optional
from sqlalchemy.orm import selectinload
from app.core.except_handler import except_handler

class AchivementRepository(TemplateRepository):

    async def create(self, name: str, description: str, amount: int)->Achievement:
        new = Achievement(name = name, description = description, amount = amount)
        self.db.add(new)
        await self.db.commit()
        await self.db.refresh(new)
        return new

    async def get_by_name(self, name: str)->list[Achievement]:
        stmt = (
            select(Achievement)
            .where(Achievement.name == name)
        )
        result = await self.db.execute(stmt)
        # Может быть несколько ачивок с одним именем? Поэтому возвращаем все
        achievements = result.scalars().all()
        return achievements

    async def get(self, id: int):
        stmt = (
            select(Achievement)
            .where(Achievement.id == id)
            .options(
                selectinload(Achievement.students)
            )
        )
        result = await self.db.execute(stmt)
        achievement = result.scalars().first()
        return achievement


    async def delete(self, id: int) -> bool:
        try:
            achievement = await self.get(id)
            await self.db.delete(achievement)
            await self.db.commit()
            return True
        except:
            return False


    async def update(self, achievement: Achievement,
                     name: Optional[str] = None,
                     description: Optional[str] = None,
                     amount: Optional[int] = None,):
        if name is not None:
            achievement.name = name
        if description is not None:
            achievement.description = description
        if amount is not None:
            achievement.amount = amount
        await self.db.commit()
        await self.db.refresh(achievement)
        return achievement



    async def give(self, achieve: Achievement, student: Student):
        achieve.students.append(student)
        await self.db.commit()
        await self.db.refresh(achieve)
        return achieve

    async def revoke(self, achieve: Achievement, student: Student)->bool:
        try:
            print("achieve", achieve, "student", student)
            achieve.students.remove(student)
            await self.db.commit()
            await self.db.refresh(achieve)
            return True
        except:
            return False


    async def get_filtered(self, name: Optional[str] = None,
                           description: Optional[str] = None,
                           amount: Optional[int] = None,
                          ) -> list[Achievement]:
        stmt = select(Achievement)

        filters = []
        if name is not None:
            filters.append(Achievement.name == name)
        if amount is not None:
            filters.append(Achievement.amount == amount)
        if description is not None:
            filters.append(Achievement.description.contains(description))
        if filters:
            stmt = stmt.where(and_(*filters))

        result = await self.db.execute(stmt)
        return result.scalars().all()



    async def get_all(self)->list[Achievement]:
        data = select(Achievement)
        achievements = await self.db.execute(data)
        return achievements.scalars().all()
