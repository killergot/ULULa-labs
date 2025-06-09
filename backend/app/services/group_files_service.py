import io
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
from app.utils.s3 import delete_file_from_s3, upload_file_to_s3, download_file_from_s3
from fastapi.responses import StreamingResponse



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

        try:
            # Формируем ключ файла в S3
            s3_key = f"{file.group.group_id}_{file.subject.id}_{file.filename}"

            # Получаем файл из S3
            original_filename, file_content = download_file_from_s3(
                file_key=s3_key,
                expected_group=str(file.group.group_id),
                expected_subject=str(file.subject.id)
            )

            # Возвращаем файл как поток
            return StreamingResponse(
                io.BytesIO(file_content),
                media_type='application/octet-stream',
                headers={'Content-Disposition': f'attachment; filename="{original_filename}"'}
            )

        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to download file: {str(e)}"
            )



    async def upload_multiple(self, files: List[UploadFile], info: FileBase):
        saved_files = []
        group = await self._get_group(info.group_number)
        subject = await self._get_subject(info.subject)

        for file in files:
            # Читаем содержимое файла
            file_content = await file.read()

            # Загружаем файл в S3
            s3_key = upload_file_to_s3(
                file_content=file_content,
                original_name=file.filename,
                group_number=str(group.group_id),
                subject=str(subject.id)
            )

            # Создаем запись в БД
            bd_file = await self.repo.create(
                group_id=group.group_id,
                subject_id=subject.id,
                filename=file.filename,
                filesize=file.size
            )

            saved_files.append(FileOut(
                id=bd_file.id,
                group_number=info.group_number,
                subject=info.subject,
                filename=file.filename,
                filesize=file.size
            ))

        return {"uploaded_files": saved_files}

    async def delete(self, file_id: int):
        file = await self._get(file_id)

        # Формируем ключ файла в S3
        s3_key = f"{file.group.group_id}_{file.subject.id}_{file.filename}"

        # Удаляем файл из S3
        if not delete_file_from_s3(s3_key):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete file from storage"
            )

        # Удаляем запись из БД
        if not await self.repo.delete(file.id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        return {"status": "success", "message": "File deleted successfully"}
