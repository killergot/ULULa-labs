import logging
from sqlalchemy import select
from uuid import UUID
from app.database.models.schedule import Schedule
from app.database.models.groups import Group
from app.repositoryes.template import TemplateRepository
from app.core.except_handler import except_handler
from app.shemas.schedule import ScheduleIn, ScheduleBase

log = logging.getLogger(__name__)

class Repository(TemplateRepository):
    async def get_by_group_id(self, group_id: int, week_number: int):
        data = select(Schedule).where(Schedule.group_id == group_id, Schedule.week_number == week_number)
        schedule = await self.db.execute(data)
        return schedule.scalars().all()


    async def create(self, schedule: ScheduleBase):
        new_schedule = Schedule(
            group_id = schedule.group_id,
            week_number = schedule.week_number,
            monday =  schedule.monday,
            tuesday = schedule.tuesday,
            wednesday = schedule.wednesday,
            thursday = schedule.thursday,
            friday = schedule.friday,
            saturday = schedule.saturday,
            sunday = schedule.sunday
        )

        self.db.add(new_schedule)
        await self.db.commit()
        await self.db.refresh(new_schedule)

    async def update(self, new_schedule: ScheduleBase):
        schedule = await self.get_by_group_id(new_schedule.group_id, new_schedule.week_number)
        schedule = schedule[0]
        schedule.monday = new_schedule.monday
        schedule.tuesday = new_schedule.tuesday
        schedule.wednesday = new_schedule.wednesday
        schedule.thursday = new_schedule.thursday
        schedule.friday = new_schedule.friday
        schedule.saturday = new_schedule.saturday
        schedule.sunday = new_schedule.sunday
        await self.db.commit()
        await self.db.refresh(schedule)
        return schedule


    @except_handler
    async def delete(self, group_id: int, week_number: int) -> bool:
        schedule = (await self.get_by_group_id(group_id, week_number))[0]
        await self.db.delete(schedule)
        await self.db.commit()
        return True


    async def get_all(self):
        data = select(Schedule)
        schedule = await self.db.execute(data)
        return schedule.scalars().all()
