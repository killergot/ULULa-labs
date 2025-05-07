from app.repositoryes.task_repository import Repository
from sqlalchemy.ext.asyncio import AsyncSession
from app.shemas.tasks import TaskIn, TaskUpdate

from fastapi import  HTTPException, status

class TaskService:
    def __init__(self, db: AsyncSession):
        self.repo = Repository(db)

    async def create_task(self, task: TaskIn):
        new_task = await self.repo.create(task.user_id, task.deadline, task.description, task.task_flag)
        return new_task

    async def get_by_user(self, user_id: int):
        new_task = await self.repo.get_by_user_id(user_id)
        if new_task:
            return new_task
        else:
            return "No tasks"

    async def get_by_id(self, task_id: int):
        new_task = await self.repo.get_by_id(task_id)
        if new_task:
            return new_task
        else:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Task not found")

    async def update(self, updated_task: TaskUpdate):
        task = await self.repo.get_by_id(updated_task.task_id)
        if task:
            return await self.repo.update(updated_task.task_id, updated_task.user_id, updated_task.deadline, updated_task.description, updated_task.task_flag)
        else:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Task not found")

    async def delete(self, task_id: int):
        task = await self.repo.get_by_id(task_id)
        if task:
            return await self.repo.delete(task_id)
        else:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Task not found")