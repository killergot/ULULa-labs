from app.repositoryes.submission_repository import SubmissionsRepository
from app.database.models.submissions import Submission
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import  HTTPException, status

class SubmissionService:
    def __init__(self, db: AsyncSession):
        self.repo = SubmissionsRepository(db)

    async def get(self, submission_id)->Submission:
        submission = await self.repo.get(submission_id)
        if submission is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Submission not found')
        return submission