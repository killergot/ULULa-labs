from .auth import router as auth_router
from .users import router as users_router
from .students import router as students_router
from .groups import router as groups_router
from .schedule import router as schedule_router
from .tasks import router as tasks_router
from .teachers import router as teacher_router
from .subjects import router as subject_router
from .files import router as files_router
from .achievements import router as achievement_router
from .shared_links import router as shared_links_router
from app.api.admin.monitoring import router as admin_router

from fastapi.routing import APIRouter


api_router = APIRouter()
api_router.include_router(admin_router)
api_router.include_router(auth_router)
api_router.include_router(files_router)
api_router.include_router(users_router)
api_router.include_router(students_router)
api_router.include_router(groups_router)
api_router.include_router(schedule_router)
api_router.include_router(tasks_router)
api_router.include_router(teacher_router)
api_router.include_router(subject_router)
api_router.include_router(achievement_router)
api_router.include_router(shared_links_router)
