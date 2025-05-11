from uuid import UUID
from fastapi import  HTTPException, status
from app.repositoryes.schedule_repository import Repository
from app.repositoryes.group_repository import Repository as group_Repository
from app.repositoryes.subject_repository import Repository as subject_Repository
from app.repositoryes.teacher_repository import Repository as teacher_Repository
from app.repositoryes.teacher_subject_repository import Repository as teacher_subject_Repository
from sqlalchemy.ext.asyncio import AsyncSession
from app.shemas.schedule import ScheduleIn
from app.database import Student

from app.utils.get_schedule import get_groups, get_schedule
from fastapi import  HTTPException, status

class ScheduleService:
    def __init__(self, db: AsyncSession):
        self.repo = Repository(db)
        self.group_repo = group_Repository(db)
        self.subject_repo = subject_Repository(db)
        self.teacher_repo = teacher_Repository(db)
        self.teacher_subject_repo = teacher_subject_Repository(db)


    async def load_schedule(self):
        groups = await get_groups()
        await self.group_repo.clean()
        await self.group_repo.create_by_list(groups)
        groups = await self.group_repo.get_all()
        schedule, subjects, teacher_subjects, group_subjects = await get_schedule(groups[0:45])
        print (subjects)
        print(teacher_subjects)
        print(group_subjects)
        await self.repo.clean_schedule()
        await self.repo.create_by_list(schedule)
        await self.subject_repo.clean()
        await self.subject_repo.create_by_list(subjects)

        # преобразовать имена преподов и названия предметов в id
        teacher_subjects_to_insert = []
        for teacher_subject in teacher_subjects:
            #получать id препода по имени, если не существует - пропускать
            teacher_id = await self.teacher_repo.get_by_FIO(teacher_subject.FIO)
            if not teacher_id:
                continue
            #получать id предмета по названию
            subject_id = await self.subject_repo.get_by_name(teacher_subject.name)
            #добавлять в список
            teacher_subjects_to_insert.append({'teacher_id': teacher_id, 'subject_id': subject_id})
        await self.teacher_subject_repo.clean()
        await self.teacher_subject_repo.create_by_list(teacher_subjects_to_insert)





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

'''
    async def load_schedule(self, group_id, week_number):
        schedule = await self.repo.get_by_group_id(group_id, week_number)
        if not schedule:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail = "Schedule not found")

        return schedule[0]


'''



