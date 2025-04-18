from fastapi import FastAPI
import uvicorn
from starlette.middleware.sessions import SessionMiddleware

from app.middleware.cors import get_cors_middleware
from app.core.config import load_config
from app.api.routers import api_router

from app.core.logger import init_log
import logging

init_log(logging.DEBUG)

config = load_config()

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
app.include_router(api_router)
get_cors_middleware(app)


if __name__ == "__main__":
    # Для докера
    # uvicorn.run("main:app",host="0.0.0.0", reload=True)
    uvicorn.run("main:app", reload=True)