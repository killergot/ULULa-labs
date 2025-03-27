from .auth import router as auth_router
from .students import router as students_router
from .schedule import router as schedule_router
from .tasks import router as task_router
from fastapi.routing import APIRouter

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(schedule_router)
api_router.include_router(students_router)
api_router.include_router(task_router)