from fastapi import Depends, status
from fastapi.routing import APIRouter
from app.database.models.submissions import Submission
from app.api.depencies.guard import get_current_user, require_role
from app.api.depencies.services import get_submission_service
from app.api.depencies.validation import get_submission_id
from app.shemas.auth import UserOut
from app.shemas.submissions import SubmissionsID
router = APIRouter(prefix="/submissions", tags=["Submissions"])

@router.get("/get/{id}",
             status_code=status.HTTP_201_CREATED,
             summary='Get submission',
             description='Get submission by id for teacher and students.\n',
             dependencies=[Depends(get_current_user)]
            )
async def get_task(submission_schema: SubmissionsID = Depends(get_submission_id), service = Depends(get_submission_service)):
    return await service.get(submission_schema.id)
