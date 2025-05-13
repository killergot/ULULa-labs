import logging
from sqlalchemy import select, text, insert
from uuid import UUID
from app.database.models.schedule import Schedule
from app.database.models.groups import Group
from app.repositoryes.template import TemplateRepository
from app.core.except_handler import except_handler
from app.shemas.schedule import ScheduleIn, ScheduleBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.models.teacher_schedule import TeacherSchedule

log = logging.getLogger(__name__)


class Repository(TemplateRepository):

    async def clean(self):
        await self.db.commit()
        await self.db.execute(text("TRUNCATE TABLE teacher_schedule RESTART IDENTITY CASCADE"))
        await self.db.commit()

    async def create_by_list(self, schedules: list):
        #print("hello!:" ,  schedules)
        for weeks in schedules[0]:
            for schedule in weeks:
                print (schedule)
                '''
                new_schedule = Schedule(
                    teacher_id=schedule.teacher_id,
                    week_number=schedule.week_number,
                    monday=schedule.monday,
                    tuesday=schedule.tuesday,
                    wednesday=schedule.wednesday,
                    thursday=schedule.thursday,
                    friday=schedule.friday,
                    saturday=schedule.saturday,
                    sunday=schedule.sunday
                )
                self.db.add(new_schedule) '''
        stmt = insert(TeacherSchedule).values(schedules)
        await self.db.execute(stmt)
        await self.db.commit()


    async def get(self, id: int, week_number: int)->TeacherSchedule:
        stmt = \
            (select(TeacherSchedule)
            .where(TeacherSchedule.teacher_id == id, TeacherSchedule.week_number == week_number)
        )
        result = await self.db.execute(stmt)
        schedule = result.scalars().first()
        return schedule