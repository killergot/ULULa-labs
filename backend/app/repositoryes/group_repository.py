from app.repositoryes.template import TemplateRepository
import logging
from app.database.models.groups import Group
from sqlalchemy import select, text

log = logging.getLogger(__name__)


class Repository(TemplateRepository):
    async def get_by_number(self, number: str):
        data = select(Group).where(Group.group_number == number)
        groups = await self.db.execute(data)
        return groups.scalars().first()


    async def clean(self):
            await self.db.commit()
            await self.db.execute(text("TRUNCATE TABLE groups RESTART IDENTITY CASCADE"))
            await self.db.commit()

    async def create_by_list(self, numbers: list[str]):
        await self.db.commit()
        try:
            for group_number in numbers:
                new_group = Group(
                    group_number=group_number
                )
                self.db.add(new_group)
        except:
            print("Error creating groups")
        await self.db.commit()




    async def get_by_id(self, id: int):
            data = select(Group).where(Group.group_id == id)
            groups = await self.db.execute(data)
            return groups.scalars().first()


    async def create(self, group_number: str) -> Group:
        new_group = Group(
            group_number = group_number
        )
        self.db.add( new_group)
        await self.db.commit()
        await self.db.refresh( new_group)
        return {'group_id':  new_group.group_id, 'group_number': new_group.group_number}


    async def delete(self, group_number: str) -> bool:
        await self.db.delete(await self.get_by_number(group_number))
        await self.db.commit()
        return True


    async def update(self, id: int, new_group_number: str):
        group = await self.get_by_id(id)
        group.group_number = new_group_number
        await self.db.commit()
        await self.db.refresh(group)
        return group

    async def get_all(self):
        data = select(Group.group_id, Group.group_number)
        group = await self.db.execute(data)
        return [{"group_id": row.group_id, "group_number": row.group_number} for row in group]