from  app.shemas.teachers import FIO as fio_schema, WeekNumber
from  app.shemas.teacher_subject import SubjectName
from  app.shemas.achievements import AchieveID
from  app.shemas.labs import LabWorkID
from fastapi import Path
from fastapi import HTTPException
from pydantic import ValidationError

def get_week_number(week_number: int = Path(ge=1, le=4)) -> WeekNumber:
    try:
        return WeekNumber(week_number=week_number)
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid week number\n: {str(e)}"
        )


def get_FIO(FIO: str) -> fio_schema:
    try:
        return fio_schema(FIO = FIO)
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid FIO\n: {str(e)}"
        )

def get_subject_name(name: str) -> SubjectName:
    try:
        return SubjectName(name = name)
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid subject name\n: {str(e)}"
        )

def get_achieve_id(id: int) -> AchieveID:
    try:
        return AchieveID(id = id)
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid achievement id\n: {str(e)}"
        )


def get_lab_work_id(id: int) -> LabWorkID:
    try:
        return LabWorkID(id = id)
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid lab work id\n: {str(e)}"
        )