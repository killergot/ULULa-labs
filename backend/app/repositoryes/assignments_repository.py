import logging
from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import date
from app.database.models.assignments import Assignment
from app.repositoryes.template import TemplateRepository
log = logging.getLogger(__name__)

class AssignmentRepository(TemplateRepository):
    async def get_all(self)->list[Assignment]:
        data = select(Assignment)
        assignment = await self.db.execute(data)
        return assignment.scalars().all()

    async def create(self, group_id: int,
                     lab_id: int,
                     teacher_id: int,
                     created_at: date,
                     deadline_at: date,
                     status: int)->Assignment:
        new_assignment = Assignment(lab_id=lab_id, group_id=group_id,
                            teacher_id=teacher_id, created_at=created_at,
                            deadline_at=deadline_at, status=status)
        self.db.add(new_assignment)
        await self.db.commit()
        await self.db.refresh(new_assignment)
        return new_assignment

    async def get(self, id: int)->Assignment:
        data = (
            select(Assignment)
            .where(Assignment.id == id)
        )
        result = await self.db.execute(data)
        assignment = result.scalars().first()
        return assignment