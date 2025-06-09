import datetime
import logging
from sqlalchemy import select, and_
from datetime import date
from app.database.models.assignments import Assignment
from app.repositoryes.template import TemplateRepository
from typing import Optional
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

    async def get_filtered(self, group_id: Optional[int] = None,
                            lab_id: Optional[int] = None,
                            teacher_id: Optional[int] = None,
                            created_at: Optional[datetime.datetime] = None,
                            deadline_at: Optional[datetime.datetime] = None,
                            status: Optional[int] = None) -> list[Assignment]:
        data = select(Assignment)

        filters = []
        if group_id is not None:
            filters.append(Assignment.group_id == group_id)
        if lab_id is not None:
            filters.append(Assignment.lab_id == lab_id)
        if status is not None:
            filters.append(Assignment.status == status)
        if teacher_id is not None:
            filters.append(Assignment.teacher_id == teacher_id)
        if created_at is not None:
            filters.append(Assignment.created_at == created_at)
        if deadline_at is not None:
            filters.append(Assignment.deadline_at == deadline_at)
        if filters:
            data = data.where(and_(*filters))
        result = await self.db.execute(data)
        return result.scalars().all()