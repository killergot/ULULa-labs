from  app.shemas.teachers import FIO as fio_schema, WeekNumber
from  app.shemas.teacher_subject import SubjectName
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