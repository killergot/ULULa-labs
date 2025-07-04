import os

from fastapi import FastAPI, Request, HTTPException
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import JSONResponse

from app.api.admin.admin_panel import setup_admin
from app.api.depencies.guard import get_current_user, get_access_token_payload
from app.database import engine
from app.database.psql import AsyncSessionLocal
from app.middleware.cors import get_cors_middleware
from app.core.config import load_config
from app.api.routers import api_router
from app.services.user_service import UserService

from app.utils.logger import init_log
import logging

from app.services.role_service import ADMIN_ROLE

init_log(logging.INFO)

config = load_config()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = FastAPI(
    title="Ulula labs",
    description="-",
    version="0.0.2",
    contact={
        "name": "Rubick",
        "email": "m.rubick@icloud.com",
    }
)
app.add_middleware(SessionMiddleware, secret_key=config.secret_keys.yandex)
# app.add_middleware(AdminAuthMiddleware)
@app.middleware("http")
async def admin_auth_middleware(request: Request, call_next):
    print('admin middleware')
    if request.url.path.startswith("/admin"):
        try:
            token = request.cookies.get("admin_token")
            if not token:
                raise HTTPException(status_code=401, detail="Not authenticated")

            payload = await get_access_token_payload(token=token)
            user_service = UserService(AsyncSessionLocal())
            user = await get_current_user(payload=payload, service=user_service)

            if not (user.role & 4):
                raise HTTPException(status_code=403, detail="Forbidden: insufficient permissions")

            request.state.user = user

        except HTTPException as http_exc:
            return JSONResponse(
                status_code=http_exc.status_code,
                content={"detail": http_exc.detail}
            )
        except Exception as exc:
            # Логировать при необходимости
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"}
            )

    return await call_next(request)

app.include_router(api_router)
get_cors_middleware(app)
setup_admin(app, engine)


if __name__ == "__main__":
    # Для докера
    # uvicorn.run("main:app",host="0.0.0.0", reload=True)
    uvicorn.run("main:app", reload=True)