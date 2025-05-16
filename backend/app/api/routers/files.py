# Что хотим уметь для сущности группы
from typing import List, Annotated, Optional

# 1 ++ - добавлять(post) новую группу (только для админов) - вход - номер группы, выход - успех/неуспех
# 2 ++ - удалять(delete) группу(только для админов) - вход - номер группы, выход - успех/неуспех
# 3.1 ++ - изменять(patch) номер группы по её id(только для админов) - вход-id группы, номер новый, выход -  успех/неуспех
# 3.2 ++- изменять(patch) номер группы по её yjvthe(только для админов) - вход-номер группы, номер новый, выход -  успех/неуспех
# 4 ++ - получать(get) номер группы по её id (для зареганых юзеров), вход - id группы, выход - номер группы
# 5 ++- получать(get) id группы по её номеру (для зареганых юзеров), вход - номер группы, выход - id группы
# 6 ++- получать список всех групп



from fastapi.routing import APIRouter
from fastapi import Depends, status, UploadFile, File,Form,Query

from app.database.models.auth import User
from app.services.group_files_service import GroupFilesService
from app.services.role_service import TEACHER_ROLE
from app.shemas.groups import FileBase, FilesFilteredIn
from app.api.depencies.guard import get_current_user, require_role
from app.api.depencies.services import get_files_service

router = APIRouter(prefix="/files", tags=["files"])

def file_base_as_form(
    group_number: str = Form(...),
    subject: str = Form(...)
) -> FileBase:
    return FileBase(group_number=group_number, subject=subject)


def get_filters(
    group_number: Optional[str] = Query(default=None, min_length=1),
    subject: Optional[str] = Query(default=None, min_length=1),
    max_filesize: Optional[int] = Query(default=None, ge=0)
) -> FilesFilteredIn:
    return FilesFilteredIn(
        group_number=group_number,
        subject=subject,
        max_filesize=max_filesize
    )

@router.post("",
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_role(TEACHER_ROLE))]
)
async def load_file(info: Annotated[FileBase, Depends(file_base_as_form)],
                    files: List[UploadFile] = File(...),
                    service: GroupFilesService = Depends(get_files_service)):
    return await service.upload_multiple(files,info)

@router.get("", status_code=status.HTTP_200_OK,
             dependencies=[Depends(get_current_user)])
async def get(
    info: Annotated[FilesFilteredIn, Depends(get_filters)],
    service: GroupFilesService = Depends(get_files_service)
):
    return await service.get_filtered(info)

@router.get("/download/{file_id}", status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user)])
async def download(
        file_id: int,
        service: GroupFilesService = Depends(get_files_service)
):
    return await service.download(file_id)

@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_role(TEACHER_ROLE))])
async def delete(
        file_id: int,
        service: GroupFilesService = Depends(get_files_service)
):
    await service.delete(file_id)

