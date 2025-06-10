import logging
from sqlalchemy import select,  and_
from datetime import date
from app.database.models.submissions import Submission
from app.repositoryes.template import TemplateRepository
from typing import Optional
log = logging.getLogger(__name__)

class SubmissionsRepository(TemplateRepository):
    async def get_all(self)->list[Submission]:
        data = select(Submission)
        submissions = await self.db.execute(data)
        return submissions.scalars().all()

    async def create(self, assignment_id: int,
                     student_id: int,
                     status: int,
                     mark: int,
                     comment: str)->Submission:
        try:
            new_submission = Submission(assignment_id=assignment_id,
                                        student_id=student_id,
                                        status=status,
                                        mark=mark,
                                        comment=comment,
                                        level=3
                                        )
            self.db.add(new_submission)
            await self.db.commit()
            await self.db.refresh(new_submission)
            return new_submission
        except Exception as e:
            print("ERROR create submission: ", e)

    async def get(self, id: int)->Submission:
        data = (
            select(Submission)
            .where(Submission.id == id)
        )
        result = await self.db.execute(data)
        submission = result.scalars().first()
        return submission


    async def update(self, submission: Submission,
                     assignment_id: Optional[int] = None,
                     student_id: Optional[int] = None,
                     status: Optional[int] = None,
                     mark: Optional[int] = None,
                     comment: Optional[str] = None,
                     level: Optional[int] = None
                     ):
        if assignment_id is not None:
            submission.assignment_id = assignment_id
        if student_id is not None:
            submission.student_id = student_id
        if status is not None:
            submission.status = status
        if mark is not None:
            submission.mark = mark
        if comment is not None:
            submission.comment = comment
        if level is not None:
            submission.level = level

        await self.db.commit()
        await self.db.refresh(submission)

    async def get_filtered(self, assignment_id: Optional[int] = None,
                           student_id: Optional[int] = None,
                           status: Optional[int] = None,
                           mark: Optional[int] = None,
                           comment: Optional[str] = None,

                           ) -> list[Submission]:
        data = select(Submission)

        filters = []
        if assignment_id is not None:
            filters.append(Submission.assignment_id == assignment_id)
        if student_id is not None:
            filters.append(Submission.student_id == student_id)
        if status is not None:
            filters.append(Submission.status == status)
        if mark is not None:
            filters.append(Submission.mark == mark)
        if comment is not None:
            filters.append(Submission.comment == comment)
        if filters:
            data = data.where(and_(*filters))

        result = await self.db.execute(data)
        return result.scalars().all()
