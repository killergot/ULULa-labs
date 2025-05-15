from typing import Optional

from app.repositoryes.template import TemplateRepository
import logging
from app.database import GroupFile
from sqlalchemy import select
from sqlalchemy import and_

log = logging.getLogger(__name__)


class GroupItemsRepository(TemplateRepository):
    async def get(self, id: int) -> GroupFile:
        return await self.db.get(GroupFile, id)

    async def get_filtered(self, group_id: Optional[int] = None,
                           subject_id: Optional[int] = None,
                           max_filesize: Optional[int] = None) -> list[GroupFile]:
        stmt = select(GroupFile)

        filters = []
        if group_id is not None:
            filters.append(GroupFile.group_id == group_id)
        if subject_id is not None:
            filters.append(GroupFile.subject_id == subject_id)
        if max_filesize is not None:
            filters.append(GroupFile.filesize <= max_filesize)

        if filters:
            stmt = stmt.where(and_(*filters))

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, group_id: int, subject_id: int, filename: str, filesize: int) -> GroupFile:
        new_file = GroupFile(group_id=group_id,
                             subject_id=subject_id,
                             filename=filename,
                             filesize=filesize)

        self.db.add(new_file)
        await self.db.commit()
        await self.db.refresh(new_file)
        return new_file

    async def bulk_create(self, group_files: list[GroupFile]) -> list[GroupFile]:
        self.db.add_all(group_files)
        try:
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            raise e
        return group_files



    async def delete(self, file_id: int) -> Optional[bool]:
        file = await self.get(file_id)
        await self.db.delete(file)
        await self.db.commit()
        return True