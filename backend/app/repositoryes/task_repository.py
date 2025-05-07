from app.repositoryes.template import TemplateRepository
import logging
from app.database.models.tasks import Task
from sqlalchemy import select

log = logging.getLogger(__name__)


# Получение по id задачи
# Создание задачи
# Удаление задачи
# Изменение задачи
class Repository(TemplateRepository):
    async def get_by_id(self, id: int):
        data = select(Task).where(Task.task_id == id)
        tasks = await self.db.execute(data)
        return tasks.scalars().first()

    async def create(self, user_id, deadline, description, task_flag) -> Task:
        new_task = Task(
            user_id = user_id,
            deadline = deadline,
            description = description,
            task_flag = task_flag
        )
        self.db.add(new_task)
        await self.db.commit()
        await self.db.refresh( new_task)
        return new_task


    async def get_by_user_id(self, user_id: int):
        data = select(Task).where(Task.user_id ==user_id)
        tasks = await self.db.execute(data)
        return tasks.scalars().all()


    async def update(self,  task_id,  user_id, deadline, description, task_flag) -> Task:
        print (type(user_id))
        task = await self.get_by_id(task_id)
        task.user_id = user_id
        task.deadline = deadline
        task.description = description
        task.task_flag = task_flag
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete(self, task_id: int) -> bool:
        await self.db.delete(await self.get_by_id(task_id))
        await self.db.commit()
        return True