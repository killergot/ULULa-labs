import os

from fastapi import FastAPI, Request, HTTPException
import uvicorn
from starlette.middleware.sessions import SessionMiddleware

from app.api.admin.admin_panel import setup_admin
from app.api.depencies.guard import get_current_user
from app.database import engine
from app.middleware.admin import AdminAuthMiddleware
from app.middleware.cors import get_cors_middleware
from app.core.config import load_config
from app.api.routers import api_router

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
app.add_middleware(AdminAuthMiddleware)

app.include_router(api_router)
get_cors_middleware(app)
setup_admin(app, engine)



if __name__ == "__main__":
    # Для докера
    # uvicorn.run("main:app",host="0.0.0.0", reload=True)
    uvicorn.run("main:app", reload=True)