from fastapi import HTTPException, status, Depends,Response
from fastapi.security import HTTPBearer


from sqlalchemy.ext.asyncio import AsyncSession

from app.repositoryes.two_factor_repository import TwoFactorRepository
from app.repositoryes.user_repository import UserRepository
from app.repositoryes.user_session_repository import UserSessionRepository
from app.utils.hash import get_hash
from app.core.security import create_access_token, create_refresh_token
from app.shemas.auth import UserIn, UserOut, TokenOut, UserLogin, TwoFactorIn, TwoFactorOut, UserBase
from app.utils.twafa import generate_2fa_code, generate_session_token, send_2fa_email

from datetime import datetime, timedelta
import ipaddress

# Глобальный словарь для хранения неудачных попыток (в реальном проекте используйте Redis или БД)
failed_attempts = {}

def record_failed_attempt(ip: str):
    """Записываем неудачную попытку входа"""
    now = datetime.now()

    # Очищаем старые записи
    for ip_addr in list(failed_attempts.keys()):
        if now - failed_attempts[ip_addr]["last_attempt"] > timedelta(minutes=30):
            del failed_attempts[ip_addr]

    # Добавляем новую запись
    if ip not in failed_attempts:
        failed_attempts[ip] = {"count": 0, "last_attempt": now}

    failed_attempts[ip]["count"] += 1
    failed_attempts[ip]["last_attempt"] = now

    # Логируем подозрительную активность
    if failed_attempts[ip]["count"] >= 3:
        print(f"WARNING: Multiple failed attempts from IP {ip}")


def is_blocked(ip: str) -> bool:
    """Проверяем, заблокирован ли IP"""
    if ip in failed_attempts:
        return failed_attempts[ip]["count"] >= 5  # Блокируем после 5 неудачных попыток
    return False


class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
        self.repo_twofa = TwoFactorRepository(db)
        self.repo_session = UserSessionRepository(db)

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

    async def login_oauth(self, user: UserBase, ):
        user = await self.repo.get_by_email(user.email)
        if not user:
            user = self.repo.create(
                email=user.email,
                password=get_hash('123'),
                role=user.role,
                auth_provider=user.auth_provider,
                provider_id=user.provider_id
            )
        access_token = create_access_token(user.id, user.email, user.role)
        refresh_token = create_refresh_token(user.id)

    async def login(self, test_user: UserLogin, bg_tasks, request):
        user = await self.repo.get_by_email(test_user.email)

        client_ip = request.client.host if request else "unknown"

        if is_blocked(client_ip):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Too many failed attempts. Please try again later."
            )

        if not user or user.password != get_hash(test_user.password):
            record_failed_attempt(client_ip)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="login or password incorrect"
            )

        # Если аутентификация успешна, сбрасываем счетчик для этого IP
        if client_ip in failed_attempts:
            del failed_attempts[client_ip]

        code = generate_2fa_code()
        session_token = generate_session_token()
        session_token = await self.repo_twofa.create(code, user.id, session_token)
        bg_tasks.add_task(send_2fa_email, user.email, code)

        return {
            "session_token": session_token.session_token,
            "detail": "2FA required. Check your email."
        }

    async def verify_2fa(self, code: TwoFactorIn, response: Response):
        session = await self.repo_twofa.check_session(code.session_token)
        if not session:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Incorrect authentication credentials")
        code = await self.repo_twofa.check_code(code.code,session.user_id)
        if not code:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Incorrect code")

        user = await self.repo.get_by_id(session.user_id)

        access_token = create_access_token(user.id, user.email, user.role)
        refresh_token = create_refresh_token(user.id)

        await self.repo_session.create(user.id,refresh_token)

        response.set_cookie(
            key="admin_token",
            value=access_token,  # Или сгенерируйте отдельный токен для админки
            httponly=True,  # Защита от XSS
            secure=False,  # Только HTTPS (в production)
        )
        return TokenOut(access_token=access_token, refresh_token=refresh_token)


    async def refresh(self, payload: dict, token) -> TokenOut:
        user_id = int(payload.get('sub'))

        user = await self.repo.get_with_sessions(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="User not found")

        access_token = create_access_token(user.id, user.email, user.role)
        refresh_token = create_refresh_token(user.id)

        for i in user.sessions:
            if i.token == token:
                await self.repo_session.update(i,token=refresh_token)


        return TokenOut(access_token=access_token, refresh_token=refresh_token)

