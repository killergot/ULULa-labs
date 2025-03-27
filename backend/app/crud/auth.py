from datetime import datetime, timedelta

from authlib.common.security import generate_token
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from app.database.models.auth import User, UserSession, Pending2FASession, TwoFactorCode
from app.services.jwt import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.services.oauth import oauth
from app.shemas.auth import UserCreate
from hashlib import sha256

from app.services.twafa import generate_2fa_code, send_2fa_email, generate_session_token


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
        user.password = sha256(user.password.encode()).hexdigest()
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
    def login_pass(cls,form_data, db: Session, bg_tasks):
        # Ищем пользователя по email
        user = db.query(User).filter(User.email == form_data.username).first()

        if not user or user.password != sha256(form_data.password.encode()).hexdigest():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль",
            )

        code = generate_2fa_code()
        db.query(TwoFactorCode).filter(TwoFactorCode.user_id == user.id).delete()

        two_factor_code = TwoFactorCode(
            user_id=user.id,
            code=code,
            expires_at=datetime.utcnow() + timedelta(minutes=5)
        )
        db.add(two_factor_code)

        # Генерация сессионного токена
        session_token = generate_session_token()
        pending_session = Pending2FASession(
            session_token=session_token,
            user_id=user.id,
            expires_at=datetime.utcnow() + timedelta(minutes=5)
        )
        db.add(pending_session)

        db.commit()

        # Отправка письма в фоне
        bg_tasks.add_task(send_2fa_email, user.email, code)

        return {
            "session_token": session_token,
            "detail": "2FA required. Check your email."
        }

    @classmethod
    def verify_2fa(cls,session_token,code,db):

        # Проверка сессионного токена
        pending_session = db.query(Pending2FASession).filter(
            Pending2FASession.session_token == session_token,
            Pending2FASession.expires_at >= datetime.utcnow()
        ).first()

        if not pending_session:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Недействительная или просроченная сессия"
            )

        # Проверка кода
        valid_code = db.query(TwoFactorCode).filter(
            TwoFactorCode.user_id == pending_session.user_id,
            TwoFactorCode.code == code,
            TwoFactorCode.expires_at >= datetime.utcnow()
        ).first()

        if not valid_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный или просроченный код"
            )

        # Создание JWT токена
        access_token = create_access_token(str(pending_session.user_id))
        expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        # Сохранение сессии
        user_session = UserSession(
            user_id=pending_session.user_id,
            token=access_token,
            expires_at=expires_at
        )

        # Очистка временных данных
        db.delete(pending_session)
        db.delete(valid_code)
        db.add(user_session)
        db.commit()

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

