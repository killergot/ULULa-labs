# Что хотим уметь для сущности группы

# 1 ++ - добавлять(post) новую группу (только для админов) - вход - номер группы, выход - успех/неуспех
# 2 ++ - удалять(delete) группу(только для админов) - вход - номер группы, выход - успех/неуспех
# 3.1 ++ - изменять(patch) номер группы по её id(только для админов) - вход-id группы, номер новый, выход -  успех/неуспех
# 3.2 ++- изменять(patch) номер группы по её yjvthe(только для админов) - вход-номер группы, номер новый, выход -  успех/неуспех
# 4 ++ - получать(get) номер группы по её id (для зареганых юзеров), вход - id группы, выход - номер группы
# 5 ++- получать(get) id группы по её номеру (для зареганых юзеров), вход - номер группы, выход - id группы
# 6 ++- получать список всех групп

from fastapi.routing import APIRouter
from fastapi import Depends, status
from app.shemas.groups import GroupBase, GroupID, GroupNumber
from app.api.depencies.guard import get_current_user, require_role

from backend.app.api.depencies.services import get_group_service

router = APIRouter(prefix="/groups", tags=["groups"])


@router.post("/create_group",
             status_code=status.HTTP_201_CREATED,
             summary='Register a new group',
             description='Create a new group in database. Requre group number.\n',
             dependencies=[Depends(get_current_user)] #заменить на закомментированную строку, чтобы работало только от админа
             #dependencies=[Depends(require_role(1))
)
async def create_group(group_number: GroupNumber, service = Depends(get_group_service)):
    return await service.create_group(group_number)


@router.delete("/delete_group",
             status_code=status.HTTP_200_OK,
             summary='Delete group',
             description='Delete group by group number.\n',
             dependencies=[Depends(get_current_user)] #заменить на закомментированную строку, чтобы работало только от админа
             #dependencies=[Depends(require_role(1))
)
async def delete_group(group_number: GroupNumber, service = Depends(get_group_service)):
    return await service.delete_group(group_number)


@router.patch("/update_group_by_id",
             status_code=status.HTTP_200_OK,
             summary='Update group',
             description='Update group by group id.\n',
             dependencies=[Depends(get_current_user)] #заменить на закомментированную строку, чтобы работало только от админа
             #dependencies=[Depends(require_role(1))
)
async def update_group_by_id(group: GroupBase, service = Depends(get_group_service)):
    return await service.update_group_by_id(group)


@router.patch("/update_group_by_number",
             status_code=status.HTTP_200_OK,
             summary='Update group',
             description='Update group by group number.\n',
             dependencies=[Depends(get_current_user)] #заменить на закомментированную строку, чтобы работало только от админа
             #dependencies=[Depends(require_role(1))
)
async def update_group_by_id(old_number: GroupNumber, new_number: GroupNumber, service = Depends(get_group_service)):
    return await service.update_group_by_number(old_number, new_number)


@router.get("/get_group_id/{group_number}",
             status_code=status.HTTP_200_OK,
             summary='Get group id',
             description='Get group id by group number.\n',
             dependencies=[Depends(get_current_user)] #заменить на закомментированную строку, чтобы работало только от админа
             #dependencies=[Depends(require_role(1))
)
async def get_group_by_number(group_number: str,service = Depends(get_group_service)):
    valid_number = GroupNumber.model_validate({"group_number": group_number})
    return await service.get_by_number(valid_number)


@router.get("/get_group_number/{group_id}",
             status_code=status.HTTP_200_OK,
             summary='Get group number',
             description='Get group number by group id.\n',
             dependencies=[Depends(get_current_user)] #заменить на закомментированную строку, чтобы работало только от админа
             #dependencies=[Depends(require_role(1))
)
async def get_group_by_number(group_id: int,service = Depends(get_group_service)):
    valid_id = GroupID.model_validate({"group_id": group_id})
    return await service.get_by_id(valid_id)


@router.get("/get_all",
             status_code=status.HTTP_200_OK,
             summary='Get group number',
             description='Get group number by group id.\n',
             dependencies=[Depends(get_current_user)] #заменить на закомментированную строку, чтобы работало только от админа
             #dependencies=[Depends(require_role(1))
)
async def get_all(service = Depends(get_group_service)):
       return await service.get_all()