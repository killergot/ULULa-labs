from tokenize import group

from fastapi import UploadFile, File
from fastapi.responses import FileResponse
import os
import shutil
from typing import List

from fastapi import  HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositoryes.group_files_repository import GroupFilesRepository
from app.shemas.groups import FilesFilteredIn, FileBase, FileOut
from app.repositoryes.group_repository import Repository as GroupRepository
from app.repositoryes.subject_repository import Repository as SubjectRepository

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class GroupFilesService:
    def __init__(self, db: AsyncSession):
        self.repo = GroupFilesRepository(db)
        self.group_repo = GroupRepository(db)
        self.subject_repo = SubjectRepository(db)

    async def _get(self, id: int):
        file = await self.repo.get(id)
        if not file:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"File with id {id} not found")
        return file

    async def _get_group(self, number: str):
        group = await self.group_repo.get_by_number(number)
        if not group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Group with id {number} not found")
        return group

    async def _get_subject(self, name: str):
        subject = await self.subject_repo.get_by_name(name)
        if not subject:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Subject with id {name} not found")
        return subject


    async def get_filtered(self, file: FilesFilteredIn):
        group = await self._get_group(file.group_number)
        subject = await self._get_subject(file.subject)
        files = await self.repo.get_filtered(group.group_id,
                                             subject.id,
                                             file.max_filesize)
        return files


    async def download(self, file_id: int):
        file = await self._get(file_id)
        file_path = os.path.join(UPLOAD_FOLDER,
                                 file.subject.name,
                                 file.group.group_number.replace('/','_'),
                                 file.filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail="Internal error, please try again later")
        return FileResponse(path=file_path, filename=file.filename, media_type='application/octet-stream')


    async def upload_multiple(self, files: List[UploadFile], info: FileBase ):
            saved_files = []
            group = await self._get_group(info.group_number)
            subject = await self._get_subject(info.subject)
            folder = os.path.join(UPLOAD_FOLDER, info.subject, info.group_number.replace('/','_'))
            os.makedirs(folder, exist_ok=True)
            for file in files:
                bd_file = await self.repo.create(group.group_id, subject.id, file.filename, file.size)
                file_location = os.path.join(folder, file.filename)
                with open(file_location, "wb") as f:
                    shutil.copyfileobj(file.file, f)
                saved_files.append(FileOut(id=bd_file.id,
                                           group_number=info.group_number,
                                           subject=info.subject,
                                           filename=file.filename,
                                           filesize=file.size))
            return {"uploaded_files": saved_files}

    async def delete(self, file_id: int):
        file = await self._get(file_id)
        folder = os.path.join(UPLOAD_FOLDER,file.subject.name, file.group.group_number.replace('/', '_'),file.filename)
        os.remove(folder)
        if not await self.repo.delete(file.id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)






