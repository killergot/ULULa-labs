from uuid import UUID

from fastapi import  HTTPException, status

from app.database.models.auth import UserSession
from app.repositoryes.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositoryes.user_session_repository import UserSessionRepository
from app.shemas.auth import UserOut, UserUpdateIn
from app.utils.hash import get_hash
from app.database import User


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
        self.repo_session = UserSessionRepository(db)

    async def _get_user(self, user_id: int) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
        return user

    async def get_user_by_email(self, email: str):
        user = await self.repo.get_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
        return UserOut.model_validate(user)

    async def get_user_by_id(self, id: int):
        user = await self._get_user(id)
        return UserOut.model_validate(user)

    async def get_all_users(self):
        users = await self.repo.get_all()
        result = [{'id': user.id, 'email': user.email, 'role': user.role} for user in users]
        return result

    async def del_user_by_id(self, id: int):
        _ = await self._get_user(id)
        if not await self.repo.delete(id):
            raise HTTPException(status_code=status.HTTP_500_NOT_FOUND,
                                detail="Error deleting user")

    async def update_user(self, user: UserUpdateIn, user_id: int):
        temp = await self._get_user(user_id)
        new_password = get_hash(user.new_password) if user.new_password else temp.password
        old_password = get_hash(user.old_password)
        if old_password != temp.password:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Wrong password")
        user = await self.repo.update(temp,  new_password)
        return UserOut.model_validate(user)

    async def get_sessions(self, user: int):
        sessions = await self.repo.get_with_sessions(user)
        if not sessions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
        return sessions.sessions

    async def delete_session(self, session_id: int):
        session = await self.repo_session.get(session_id)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Session not found")
        if not await self.repo_session.delete(session):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Error deleting session")