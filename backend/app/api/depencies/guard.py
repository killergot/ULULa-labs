from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from app.api.depencies.services import get_user_service
from app.core.security import decode_access_token, decode_refresh_token
from app.services.user_service import UserService
from app.shemas.auth import UserOut

security = HTTPBearer()

async def get_token_from_header(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    return credentials.credentials

async def get_access_token_payload(
    token: str = Depends(get_token_from_header)
) -> dict:
    payload = decode_access_token(token)
    if not payload or "id" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid access token payload")
    return payload

async def get_refresh_token_payload(
    token: str = Depends(get_token_from_header),
    service = Depends(get_user_service)
) -> dict:

    payload = decode_refresh_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid refresh token payload")

    sessions = await service.get_sessions(int(payload["sub"]))
    for i in sessions:
        if i.token == token:
            return payload
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid refresh token payload")

async def get_current_user(
    payload: dict = Depends(get_access_token_payload),
    service: UserService = Depends(get_user_service)
) -> UserOut:
    user: UserOut = await service.get_user_by_id(payload["id"])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User not found")
    return user

def require_role(req_role: int):
    async def role_checker(payload: dict = Depends(get_access_token_payload)):
        print(payload['role'])
        if not payload["role"] & req_role:
            raise HTTPException(status_code=403,
                                detail="Not enough permissions")
        return payload
    return role_checker