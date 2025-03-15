from fastapi import FastAPI, HTTPException
from typing import List,Optional
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from validation.users import UserSignIn,UserSignUp
from sqlalchemy import create_engine,  MetaData, Table, insert, select
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import Session




app = FastAPI()


def connection_to_db():
    engine = create_engine("postgresql://ulula_server_admin:ulula_server_password@localhost/ulula_helper_db")
    print(database_exists(engine.url))
    return engine

def insert_to_general_users(mail, passw, role):
    engine = connection_to_db()
    metadata = MetaData()
    # Отражение существующей таблицы
    table = Table("uses_general_table", metadata, autoload_with=engine)
    with engine.connect() as connection:
       stmt = insert(table).values(email=mail, role=int(3), passsword=passw)
       print (mail, passw, role)
       connection.execute(stmt)
       connection.commit()
    engine.dispose()

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
    engine = connection_to_db()
    metadata = MetaData()
    # Отражение существующей таблицы
    table = Table("uses_general_table", metadata, autoload_with=engine)
    with engine.connect() as connection:
       query = select(table.c.role, table.c.passsword).where(table.c.email == email)
       rez = connection.execute(query)
       connection.commit()
    #engine.dispose()
    result_list = [row._asdict() for row in rez]
    if not result_list:
            return None
    return result_list[0]

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
    try:
        #connection_to_db()
        insert_to_general_users(user_data.email, user_data.password, user_data.role)
    except Exception as e:
        return {"message": "error"+str(e)}
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
    if user["passsword"] != credentials.password:
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )

    return {
        "message": "Login successful",
        "user": {
            "email": credentials.email,
            "role": user["role"]
        }
    }

@app.get("/all_users")
async def sign():
    return users

if __name__ == "main":
    uvicorn.run("main:app")