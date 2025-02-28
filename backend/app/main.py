from fastapi import FastAPI, HTTPException
from typing import List,Optional
from fastapi.middleware.cors import CORSMiddleware

from .validation.users import UserSignIn,UserSignUp

app = FastAPI()

#CORS нужен для связки front'a и back'а
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все домены
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

# Временное хранилище пользователей в памяти
users: List[dict] = []

# Вспомогательные функции
def find_user_by_email(email: str) -> Optional[dict]:
    return next((user for user in users if user["email"] == email), None)


# Ручки API
@app.post("/signup")
async def signup(user_data: UserSignUp):
    # Проверка существования пользователя
    if find_user_by_email(user_data.email):
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )

    # Создание нового пользователя
    new_user = {
        "email": user_data.email,
        "password": user_data.password,  # В реальном приложении нужно хэшировать!
        "role": user_data.role
    }

    users.append(new_user)
    return {"message": "User created successfully"}


@app.post("/signin")
async def signin(credentials: UserSignIn):
    # Поиск пользователя
    user = find_user_by_email(credentials.email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Проверка пароля
    if user["password"] != credentials.password:
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )

    return {
        "message": "Login successful",
        "user": {
            "email": user["email"],
            "role": user["role"]
        }
    }

@app.get("/all_users")
async def sign():
    return users