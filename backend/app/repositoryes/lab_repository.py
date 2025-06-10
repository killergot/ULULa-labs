import logging
from typing import Optional
from sqlalchemy import select, and_
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

    async def get_filtered(self, title: Optional[str] = None,
                           description: Optional[str] = None,
                           subject_id: Optional[int] = None,
                           created_by: Optional[int] = None,
                           file_id: Optional[int]=None) -> list[LabWork]:
        data = select(LabWork)

        filters = []
        if title is not None:
            filters.append(LabWork.title == title)
        if description is not None:
            filters.append(LabWork.description == description)
        if subject_id is not None:
            filters.append(LabWork.subject_id == subject_id)
        if created_by is not None:
            filters.append(LabWork.created_by == created_by)
        if file_id is not None:
            filters.append(LabWork.file_id == file_id)

        if filters:
            data = data.where(and_(*filters))
        result = await self.db.execute(data)
        return result.scalars().all()