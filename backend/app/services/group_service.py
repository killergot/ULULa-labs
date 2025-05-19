from app.repositoryes.group_repository import Repository
from sqlalchemy.ext.asyncio import AsyncSession
from app.shemas.groups import GroupNumber, GroupID, GroupBase
# 1 - добавлять(post) новую группу (только для админов) - вход - номер группы, выход - успех/неуспех
# 2 - удалять(delete) группу(только для админов) - вход - номер группы, выход - успех/неуспех
# 3.1 - изменять(patch) номер группы по её id(только для админов) - вход-id группы, номер новый, выход -  успех/неуспех
# 3.2 - изменять(patch) номер группы по её yjvthe(только для админов) - вход-номер группы, номер новый, выход -  успех/неуспех
# 4 - получать(get) номер группы по её id (для зареганых юзеров), вход - id группы, выход - номер группы
# 5 - получать(get) id группы по её номеру (для зареганых юзеров), вход - номер группы, выход - id группы
from fastapi import  HTTPException, status

class GroupService:
    def __init__(self, db: AsyncSession):
        self.repo = Repository(db)


    async def create_group(self, group: GroupNumber): #создаём новую группу
        #проверка, что группа ещё не существует
        if await self.repo.get_by_number(group.group_number):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Group already exist')
        #создание группы
        new_group = await self.repo.create(group.group_number)
        return 0

    async def delete_group(self, group: GroupNumber): #удаляем группу
        #проверка, что группа существует
        #print(group.group_number)
        if not await self.repo.get_by_number(group.group_number):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Group does not exist')
        #удаление группы
        return await self.repo.delete(group.group_number)

    async def update_group_by_id(self, group: GroupBase):
        existig_group = await self.repo.get_by_id(group.group_id)
        if not existig_group :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Group does not exist')
            # обновление группы
        return await self.repo.update(group.group_id, group.group_number)

    async def update_group_by_number(self, old_number: GroupNumber, new_number: GroupNumber):
        existig_group = await self.repo.get_by_number(old_number.group_number)
        if not existig_group :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Group does not exist')
            # удаление группы
        return await self.repo.update(existig_group.group_id, new_number.group_number)

    async def get_by_number(self, group_number: GroupNumber):
        exist_group = await self.repo.get_by_number(group_number.group_number)
        if not exist_group:
            print('Нет такой')
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Group does not exist')
        return exist_group.group_id

    async def get_by_id(self, group_id: GroupID):
        exist_group = await self.repo.get_by_id(group_id.group_id)
        if not  exist_group:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Group does not exist')
        return exist_group.group_number

    async def get_all(self):
        groups = await self.repo.get_all()
        if not groups:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Groups not found")
        return groups