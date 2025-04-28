from fastapi import  Depends


from sqlalchemy.ext.asyncio import AsyncSession

from app.api.depencies.db import get_db
from app.database.models.students import Student
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.student_service import StudentService
from app.services.group_service import GroupService

async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)

async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)

async def get_student_service(db: AsyncSession = Depends(get_db)) -> StudentService:
    return StudentService(db)

async def get_group_service(db: AsyncSession = Depends(get_db)) -> GroupService:
    return GroupService(db)