from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositoryes.user_repository import UserRepository
from app.utils.hash import get_hash
from app.core.security import create_access_token, create_refresh_token
from app.shemas.auth import UserIn, UserOut, TokenOut, UserLogin


class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def register(self, user: UserIn):
        if await self.repo.get_by_email(user.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Email already registered')
        # Тут возможно стоит поменять на то, что не стоит выдавать инфу о существующих пользователях
        # Точнее вообще никакой инфы, всегда отвечать ok True, чтоб нельзя было перебрать базу пользователей

        new_user = await self.repo.create(user.email,
                                          get_hash(user.password),
                                          user.role)

        return UserOut.model_validate(new_user)


    async def login(self, test_user: UserLogin):
        user = await self.repo.get_by_email(test_user.email)

        if not user or user.password != get_hash(test_user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="login or password incorrect")

        access_token = create_access_token(user.id, user.email, user.role)
        refresh_token = create_refresh_token(user.id)
        return TokenOut(access_token=access_token, refresh_token=refresh_token)

    async def refresh(self, payload: dict) -> TokenOut:
        user_id = int(payload.get('sub'))

        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="User not found")

        access_token = create_access_token(user.id, user.email, user.role)
        refresh_token = create_refresh_token(user.id)

        return TokenOut(access_token=access_token, refresh_token=refresh_token)

