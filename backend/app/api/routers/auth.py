from fastapi import Depends, status,Response, HTTPException, BackgroundTasks
from fastapi.routing import APIRouter

from app.api.depencies.guard import get_refresh_token_payload
from app.api.depencies.services import get_auth_service

from app.shemas.auth import UserOut, UserIn, UserLogin, TokenOut, TwoFactorOut, TwoFactorIn
from app.services import AuthService


router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup", response_model=UserOut,
             status_code=status.HTTP_201_CREATED,
             summary='Register a new user',
             description='Create a new user in database. Requre email and password.\n')
async def create_user(user: UserIn, service: AuthService = Depends(get_auth_service)):
    return await service.register(user)

@router.post("/login", status_code=status.HTTP_201_CREATED,
             summary='Login a user')
async def login(
        background_tasks: BackgroundTasks,user: UserLogin, service: AuthService = Depends(get_auth_service),
                ):

    return await service.login(user,background_tasks)

@router.post("/verify-2fa", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
async def login(response: Response,code: TwoFactorIn, service: AuthService = Depends(get_auth_service)):
    return await service.verify_2fa(code, response)


@router.post('/refresh', response_model=TokenOut)
async def refresh(payload: dict = Depends(get_refresh_token_payload)
                  , service: AuthService = Depends(get_auth_service)):
    return await service.refresh(payload)