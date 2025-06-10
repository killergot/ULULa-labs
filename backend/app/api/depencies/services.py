from fastapi import  Depends


from sqlalchemy.ext.asyncio import AsyncSession

from app.api.depencies.db import get_db

from app.services.auth_service import AuthService
from app.services.group_files_service import GroupFilesService
from app.services.shared_links_service import SharedLinkService
from app.services.user_service import UserService
from app.services.student_service import StudentService
from app.services.group_service import GroupService
from app.services.schedule_service import ScheduleService
from app.services.task_service import TaskService
from app.services.teacher_service import TeacherService
from app.services.subject_service import SubjectService
from app.services.achievement_service import AchievementService
from app.services.submission_service import SubmissionService

async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)

async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)

async def get_student_service(db: AsyncSession = Depends(get_db)) -> StudentService:
    return StudentService(db)

async def get_group_service(db: AsyncSession = Depends(get_db)) -> GroupService:
    return GroupService(db)

async def get_schedule_service(db: AsyncSession = Depends(get_db)) -> ScheduleService:
    return ScheduleService(db)

async def get_task_service(db: AsyncSession = Depends(get_db)) -> TaskService:
    return TaskService(db)

async def get_teacher_service(db: AsyncSession = Depends(get_db)) -> TeacherService:
    return TeacherService(db)

async def get_subject_service(db: AsyncSession = Depends(get_db)) -> SubjectService:
    return SubjectService(db)

async def get_files_service(db: AsyncSession = Depends(get_db)) -> GroupFilesService:
    return GroupFilesService(db)

async def get_achievement_service(db: AsyncSession = Depends(get_db)) -> AchievementService:
    return AchievementService(db)

async def get_shared_links_service(db: AsyncSession = Depends(get_db)) -> SharedLinkService:
    return SharedLinkService(db)

async def get_submission_service(db: AsyncSession = Depends(get_db)) -> SubmissionService:
    return SubmissionService(db)