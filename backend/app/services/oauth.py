from authlib.integrations.starlette_client import OAuth
from app.config.config import load_config

config = load_config()

YANDEX_CLIENT_ID = "a9e81891c8c742dc8cf988a6816424a6"
YANDEX_CLIENT_SECRET = config.yandex_secret
REDIRECT_URI = "http://localhost:8000/auth/callback"

oauth = OAuth()
oauth.register(
    name="yandex",
    client_id=YANDEX_CLIENT_ID,
    client_secret=YANDEX_CLIENT_SECRET,
    authorize_url="https://oauth.yandex.ru/authorize",
    access_token_url="https://oauth.yandex.ru/token",
    userinfo_endpoint="https://login.yandex.ru/info",
    client_kwargs={"scope": "login:email login:info"}
)