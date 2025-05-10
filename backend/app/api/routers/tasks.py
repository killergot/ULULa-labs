from fastapi import Depends, status
from fastapi.routing import APIRouter
from app.database.models.tasks import Task
from app.api.depencies.guard import get_current_user, require_role
from app.api.depencies.services import get_task_service
from app.services.task_service import TaskService
from app.shemas.tasks import TaskIn, TaskInShort, TaskID, TaskUpdate
from app.shemas.auth import UserOut
from app.shemas.students import StudentID
router = APIRouter(prefix="/tasks", tags=["Tasks"])

# ++ 1.1 Добавлять задачу по id пользователя
# ++ 1.2 Добавлять задачу для текущего пользователя
# ++ 2.1 Получать список задач по id пользователя
# ++ 2.2 Получать список задач текущего пользователя
# ++ 2.3 Получать конкретную задачу по id
# ++ 3 Изменять задачу по id задачи
# 4 Удалять задачу по id задачи

@router.post("/create_task",
             status_code=status.HTTP_201_CREATED,
             summary='Create new task',
             description='Create new task. For admins and teachers? (Now for any user).\n')
async def create_task(new_task: TaskIn, service = Depends(get_task_service)):
    return await service.create_task(new_task)

@router.post("/create_task_for_me",
             status_code=status.HTTP_201_CREATED,
             summary='Create new task for current user',
             description='Create task by user for himself.\n')
async def create_task(task: TaskInShort, service = Depends(get_task_service), user: UserOut = Depends(get_current_user)):
    new_task = TaskIn.model_validate({"user_id": user.id, "deadline": task.deadline, "description": task.description, "task_flag": task.task_flag})
    return await service.create_task(new_task)

@router.get("/get_tasks",
             status_code=status.HTTP_201_CREATED,
             summary='Get tasks for user for his id. For admins?',
             description='Get tasks for user by his id.\n')
async def get_tasks(user_id: int, service = Depends(get_task_service)):
    return await service.get_by_user(StudentID.model_validate({"student_id": user_id}).student_id)

@router.get("/get_tasks_for_me",
             status_code=status.HTTP_201_CREATED,
             summary='Get tasks for current user',
             description='Get tasks for current user.\n')
async def get_task(service = Depends(get_task_service), user: UserOut = Depends(get_current_user)):
    return await service.get_by_user(user.id)


@router.get("/get_task",
             status_code=status.HTTP_201_CREATED,
             summary='Get task by its id',
             description='Get task by id.\n')
async def get_task(task_id: int, service = Depends(get_task_service)):
    return await service.get_by_id(TaskID.model_validate({"task_id": task_id}).task_id)

@router.patch("/update_task",
             status_code=status.HTTP_201_CREATED,
             summary='Update task by id',
             description='Update task by id.\n')
async def update_task(task: TaskUpdate,  service: TaskService = Depends(get_task_service), user = Depends(get_current_user)):
    return await service.update(task,user.id)

@router.delete("/delete_task",
             status_code=status.HTTP_201_CREATED,
             summary='Delete task by id',
             description='Delete task by id.\n')
async def delete_task(task: TaskID,  service = Depends(get_task_service)):
    return await service.delete(task.task_id)
