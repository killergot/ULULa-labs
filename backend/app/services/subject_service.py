
from fastapi import  HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositoryes.subject_repository import Repository
from app.repositoryes.group_subject_repository import Repository as GroupSubjectRepository
from app.repositoryes.group_repository import Repository as GroupRepository



class SubjectService:
    def __init__(self, db: AsyncSession):
        self.repo = Repository(db)
        self.group_repo = GroupRepository(db)
        self.group_subject_repo =  GroupSubjectRepository(db)


    async def get_groups(self, name: str)->list[str]:
        # получить id
        subject = await self.repo.get_by_name(name)
        id = subject.id
        full_subjects = await self.group_subject_repo.get_by_subject(id)
        groups = []
        for subject in full_subjects:
            name = await self.group_repo.get_by_id(subject.group_id)
            groups.append(name.group_number)
        return groups
