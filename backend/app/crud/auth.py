from datetime import datetime, timedelta

from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from app.database.models.auth import User, UserSession
from app.services.jwt import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.services.oauth import oauth
from app.shemas.auth import UserCreate
from hashlib import sha256

class UserService:
    @classmethod
    def is_user_exist(cls,db: Session, email):
        return db.query(User).filter(User.email == email).first()

    @classmethod
    def create_user(cls,db: Session, user: UserCreate) -> User:
        # Проверка уникальности email
        if cls.is_user_exist(db, user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Проверка уникальности provider_id для OAuth
        if user.provider_id:
            if db.query(User).filter(User.provider_id == user.provider_id).first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Provider ID already exists"
                )

        # Создание объекта пользователя
        db_user = User(**user.model_dump())

        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        return db_user

    @classmethod
    def login_pass(cls,form_data, db: Session):
        # Ищем пользователя по email
        user = db.query(User).filter(User.email == form_data.username).first()

        # Проверяем пароль (рекомендуется добавить хеширование!)
        if not user or user.password != form_data.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль",
            )

        # Создаем JWT токен и сессию
        access_token = create_access_token(str(user.id))
        expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        try:
            session = UserSession(
                user_id=user.id,
                token=access_token,
                expires_at=expires_at
            )
            db.add(session)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e) + 'Какая-то ошибка при добавлении сессии пользователя в BD'
            )

        return {"access_token": access_token, "token_type": "bearer"}

    @classmethod
    async def auth_callback(cls,request,db):
        try:
            print("Авторизация началась...")
            token = await oauth.yandex.authorize_access_token(request)
            print(f"Полученный токен: {token}")

            userinfo = await oauth.yandex.get("https://login.yandex.ru/info", token=token)
            user_data = userinfo.json()
            print(f"Информация о пользователе: {user_data}")
            user = UserCreate(
                email=user_data["default_email"],
                auth_provider='yandex',
                provider_id='yandex'
            )
            UserService.create_user(db, user)
            user = db.query(User).filter(User.email == user_data["default_email"]).first()
            print(f'{user.id =}')
            try:
                session = UserSession(
                    user_id=user.id,
                    token=token['access_token'],
                    expires_at=datetime.fromtimestamp(token['expires_at'])
                )
                db.add(session)
                db.commit()
            except Exception as e:
                print('Тут какая-то поломка', e)
                db.rollback()
                raise HTTPException(
                    status_code=500,
                    detail=str(e) + 'Какая-то ошибка при добавлении сессии пользователя в BD'
                )
            return {"access_token": token, "user_data": user_data}
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="Ошибкаdsfds авторизации")

