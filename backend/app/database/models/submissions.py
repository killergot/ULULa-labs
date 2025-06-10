from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, TIMESTAMP, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.psql import Base
from datetime import datetime
from app.database.models.assignments import Assignment
from app.database.models.subjects import Subject
from app.database.models.group_files import GroupFile
from app.database.models.students import Student

class Submission(Base):
    __tablename__ = 'submissions'
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    assignment_id: Mapped[int] = mapped_column(Integer, ForeignKey('assignments.id', ondelete='CASCADE'), nullable=False)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    status: Mapped[int] = mapped_column(Integer, nullable=False) # сделал/не сделал/готов сдавать
    mark: Mapped[int] = mapped_column(Integer, nullable=False) #Оценка (1/0 или иное)
    comment: Mapped[str] = mapped_column(String(300))
     # type: ignore
    students: Mapped["database.models.students.Student"] = relationship("database.models.students.Student", back_populates="submission")
    assignment: Mapped["database.models.assignments.Assignment"] = relationship("database.models.assignments.Assignment",
                                                                          back_populates="submission")