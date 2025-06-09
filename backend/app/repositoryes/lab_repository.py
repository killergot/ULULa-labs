import logging
from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database.models.lab_works import LabWork
from app.repositoryes.template import TemplateRepository
log = logging.getLogger(__name__)

class LabsRepository(TemplateRepository):
    async def get_all(self)->list[LabWork]:
        data = select(LabWork)
        labs = await self.db.execute(data)
        return labs.scalars().all()

    async def create(self, title, description, subject_id, created_by, file_id = None)->LabWork:
        new_lab = LabWork(title=title, description=description, subject_id=subject_id, created_by=created_by, file_id=file_id)
        self.db.add(new_lab)
        await self.db.commit()
        await self.db.refresh(new_lab)
        return new_lab

    async def get(self, id: int)->LabWork:
        data = (
            select(LabWork)
            .where(LabWork.id == id)
        )
        result = await self.db.execute(data)
        lab = result.scalars().first()
        return lab