from app.api.depencies.guard import get_current_user, require_role
from app.api.depencies.services import get_subject_service
from app.shemas.students import StudentBase, StudentIn, StudentID
from app.shemas.auth import UserOut
from fastapi import Depends, status
from fastapi.routing import APIRouter

from app.api.depencies.validation import get_subject_name

from app.shemas.teacher_subject import SubjectName

router = APIRouter(prefix="/subjects", tags=["subjects"])

@router.get("/groups/{name}",
             status_code=status.HTTP_200_OK,
             summary='Get groups learning subject',
             description='Get groups learning subject.\n')
# добавить зависимость для зареганного юзера
async def get_groups(name_schema: SubjectName=Depends(get_subject_name),  service = Depends(get_subject_service))->list[str]:
    return await service.get_groups(name_schema.name)