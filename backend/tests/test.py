from fastapi import FastAPI, Depends, HTTPException
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse
import os

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="ed824e2aeb61264270ace597e10bb55f")
# Настройки OAuth2 для Mail.ru
MAILRU_CLIENT_ID = "1111"
MAILRU_CLIENT_SECRET = "1111"
REDIRECT_URI = "http://localhost:8000/auth/callback"

oauth = OAuth()
oauth.register(
    name="yandex",
    client_id=MAILRU_CLIENT_ID,
    client_secret=MAILRU_CLIENT_SECRET,
    authorize_url="https://oauth.yandex.ru/authorize",
    access_token_url="https://oauth.yandex.ru/token",
    userinfo_endpoint="https://login.yandex.ru/info",
    client_kwargs={"scope": "login:email login:info"}
)

# URL для начала авторизации
@app.get("/auth/login")
async def login(request: Request):
    redirect_uri = REDIRECT_URI
    return await oauth.yandex.authorize_redirect(request, redirect_uri)

# Callback-обработчик
@app.get("/auth/callback")
async def auth_callback(request: Request):
    try:
        print("Авторизация началась...")
        token = await oauth.yandex.authorize_access_token(request)
        print(f"Полученный токен: {token}")

        userinfo = await oauth.yandex.get("https://login.yandex.ru/info", token=token)
        user_data = userinfo.json()
        print(f"Информация о пользователе: {user_data}")
        return {"access_token": token, "user_data": user_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Ошибкаdsfds авторизации")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,log_level='debug')
