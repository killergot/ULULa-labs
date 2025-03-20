from fastapi import FastAPI
import uvicorn
from starlette.middleware.sessions import SessionMiddleware

from app.middleware.cors import get_cors_middleware
from app.api import api_router

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="ed824e2aeb61264270ace597e10bb55f")
app.include_router(api_router)
get_cors_middleware(app)



if __name__ == "main":
    uvicorn.run("main:app")