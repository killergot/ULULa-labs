from idlelib.window import add_windows_to_menu
from uuid import UUID

from fastapi import Depends, status, HTTPException
from fastapi.routing import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.depencies.guard import get_current_user, require_role
from app.api.depencies.services import get_user_service, get_shared_links_service
from app.services import user_service
from app.services.role_service import ADMIN_ROLE
from app.services.shared_links_service import SharedLinkService
from app.shemas.auth import UserOut, UserUpdateIn
from app.shemas.tasks import SharedLinkIn

router = APIRouter(prefix="/shared_links", tags=["shared_links"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_shared_link(link: SharedLinkIn,
                             user: UserOut = Depends(get_current_user),
                             service: SharedLinkService = Depends(get_shared_links_service)):
    return await service.create(link)

@router.get("", status_code=status.HTTP_200_OK)
async def get_all_my(user = Depends(get_current_user),
                     service: SharedLinkService = Depends(get_shared_links_service)):
    return await service.get_all(user.id)

@router.get("/{token}", status_code=status.HTTP_200_OK)
async def get_shared_link(token: UUID,
                          service: SharedLinkService = Depends(get_shared_links_service)):
    return await service.get_by_token(token)

@router.delete("/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shared_link(link_id: int,
                             service: SharedLinkService = Depends(get_shared_links_service),
                             user: UserOut = Depends(get_current_user)):
    return await service.delete(link_id,user.id)
