from fastapi import FastAPI
import uvicorn
from starlette.middleware.sessions import SessionMiddleware

from app.middleware.cors import get_cors_middleware
from app.config.config import load_config
from app.api import api_router

config = load_config()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=config.yandex_secret)
app.include_router(api_router)
get_cors_middleware(app)


#
# if __name__ == "__main__":
#     uvicorn.run("main:app")

