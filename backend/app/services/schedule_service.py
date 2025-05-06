from uuid import UUID
from fastapi import  HTTPException, status
from app.repositoryes.schedule_repository import Repository
from app.repositoryes.group_repository import Repository as group_Repository
from sqlalchemy.ext.asyncio import AsyncSession
from app.shemas.schedule import ScheduleIn
from app.utils.hash import get_hash
from app.database import Student


from fastapi import  HTTPException, status

class ScheduleService:
    def __init__(self, db: AsyncSession):
        self.repo = Repository(db)
        self.group_repo = group_Repository(db)



    async def create_schedule(self, schedule: ScheduleIn): # создаём расписание
        # проверка, что группа существует
        if not await self.group_repo.get_by_id(schedule.group_id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Group does not exist')
        #проверка, что расписание ещё не существует
        if await self.repo.get_by_group_id(schedule.group_id, schedule.week_number):
            print ("hello")
            new_schedule = await self.repo.update(schedule)
        else:
            new_schedule = await self.repo.create(schedule)
        return (new_schedule)


    async def delete_schedule(self, group_id: int): # создаём расписание
        # проверка, что группа существует
        if not await self.group_repo.get_by_id(group_id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Group does not exist')
        #проверка, что расписание ещё не существует
        for i in range (1, 5):
            if not await self.repo.get_by_group_id(group_id, i):
               continue
            else:
                new_schedule = await self.repo.delete(group_id, i)
        return True


    async def get_all(self):
        schedule = await self.repo.get_all()
        if not schedule:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail = "Schedule not found")

        return schedule

    async def get_by_id(self, group_id, week_number):
        schedule = await self.repo.get_by_group_id(group_id, week_number)
        if not schedule:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail = "Schedule not found")

        return schedule[0]


    async def load_schedule(self, group_id, week_number):
        schedule = await self.repo.get_by_group_id(group_id, week_number)
        if not schedule:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail = "Schedule not found")

        return schedule[0]






