from fastapi import UploadFile, File
import os
import shutil
from typing import List

from fastapi import  HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositoryes.group_files_repository import GroupFilesRepository
from app.shemas.groups import FilesFilteredIn
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

    async def get_filtered(self, file: FilesFilteredIn):
        group = await self.group_repo.get_by_number(file.group_number)
        if not group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Group with id {file.group_number} not found")
        subject = await self.subject_repo.get_by_name(file.subject)
        if not subject:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Subject with id {file.subject} not found")

        files = await self.repo.get_filtered(group.group_id,
                                             subject.id,
                                             file.max_filesize)

        return files  # ????


    async def download(self, file: FilesFilteredIn):
        pass

    async def upload_multiple(self, files: List[UploadFile] = File(...)):
        saved_files = []
        for file in files:
            file_location = os.path.join(UPLOAD_FOLDER, file.filename)
            with open(file_location, "wb") as f:
                shutil.copyfileobj(file.file, f)
            saved_files.append(file.filename)
        return {"uploaded_files": saved_files}






