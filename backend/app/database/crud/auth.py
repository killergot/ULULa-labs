from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from app.database.models.auth import User
from app.shemas.auth import UserCreate

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

