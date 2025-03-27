from datetime import datetime, timedelta

from fastapi import Depends, HTTPException,status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.requests import Request

from database.models.auth import User, UserSession
from database.psql import get_db
from services.oauth import oauth
from services.jwt import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user, oauth2_scheme
from services.oauth import REDIRECT_URI
from shemas.auth import UserCreate, UserResponse, Token
from crud.auth import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db, user)


@router.post("/login", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    return UserService.login_pass(form_data, db)


@router.get("/login_oauth")
async def login_oauth(request: Request):
    redirect_uri = REDIRECT_URI
    return await oauth.yandex.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def auth_callback(request: Request,
                        db: Session = Depends(get_db)):
    return UserService.auth_callback(request,db)

@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    # Удаляем сессию
    session = db.query(UserSession).filter(UserSession.token == token).first()
    if session:
        db.delete(session)
        db.commit()
    return {"detail": "Успешный выход"}


@router.post("/refresh", response_model=Token)
async def refresh_token(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    # Создаем новый токен
    new_access_token = create_access_token(str(current_user.id))
    expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Обновляем сессию
    session = db.query(UserSession).filter(UserSession.token == token).first()
    if session:
        session.token = new_access_token
        session.expires_at = expires_at
        db.commit()

    return {"access_token": new_access_token, "token_type": "bearer"}
