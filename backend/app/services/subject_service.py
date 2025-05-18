
from fastapi import  HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositoryes.subject_repository import Repository
from app.repositoryes.group_subject_repository import Repository as GroupSubjectRepository
from app.repositoryes.group_repository import Repository as GroupRepository
from app.repositoryes.student_repository import Repository as StudentRepository

class SubjectService:
    def __init__(self, db: AsyncSession):
        self.repo = Repository(db)
        self.group_repo = GroupRepository(db)
        self.group_subject_repo =  GroupSubjectRepository(db)
        self.student_repo = StudentRepository(db)

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


    async def get_subjects(self, id: int)->list[str]:
        try:
            # получить id группы студента
            student = await self.student_repo.get(id)
            full_subjects = await self.group_subject_repo.get_by_group(student.group_id)
            subjects = []
            for subject in full_subjects:
                name = await self.repo.get(subject.subject_id)
                subjects.append(name.name)
            return subjects
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Subjects not found")