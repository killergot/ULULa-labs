from typing import Optional
from app.database.models.achievent import Achievement
from app.api.depencies.guard import get_current_user, require_role
from app.shemas.auth import UserOut
from app.shemas.achievements import AchieveIn, AchieveID, AchieveUpdate
from fastapi import Depends, status, Query
from fastapi.routing import APIRouter
from app.api.depencies.validation import get_week_number, get_FIO, get_achieve_id
from app.api.depencies.services import get_achievement_service

router = APIRouter(prefix="/achievements", tags=["achievements"])

@router.get("/achievements/{id}",
            status_code=status.HTTP_200_OK,
            summary='Get achievement',
            description='Update achievement by id.\n',
            dependencies=[Depends(get_current_user)]
            )
async def get(id_schema: AchieveID = Depends(get_achieve_id), service = Depends(get_achievement_service)):
        achieve =  await service.get_achievement(id_schema.id)
        print (achieve.students)
        return await service.get_achievement(id_schema.id)

@router.get("/achievements/",
            status_code=status.HTTP_200_OK,
            summary='Get achievement',
            description='Update achievement by id.\n',
            dependencies=[Depends(get_current_user)]
            )
async def get(
        name: Optional[str] = Query(default = None, min_length = 1),
        description: Optional[str] = Query(default = None, min_length = 1),
        amount: Optional[int] = Query(default=None, ge=1),
        service = Depends(get_achievement_service)):
        return await service.get_filtered(name, description, amount)

