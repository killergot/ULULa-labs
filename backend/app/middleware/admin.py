from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.api.depencies.guard import (
    get_token_from_header,
    get_access_token_payload,
    get_current_user,
)
from app.database.psql import AsyncSessionLocal
from app.services.user_service import UserService  # Импорт вашего сервиса

class AdminAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/admin"):
            # Получаем токен из cookie
            token = request.cookies.get("admin_token")
            if not token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                )

            # Проверяем токен
            try:
                payload = await get_access_token_payload(token=token)
                user_service = UserService(AsyncSessionLocal())
                user = await get_current_user(payload=payload, service=user_service)
                if not user.role & 4:
                    raise HTTPException(status_code=403, detail="Forbidden")
                request.state.user = user
            except Exception as e:
                raise HTTPException(status_code=403, detail=str(e))

        return await call_next(request)