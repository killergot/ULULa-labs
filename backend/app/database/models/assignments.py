from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, TIMESTAMP, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.psql import Base
from datetime import datetime
from app.database.models.lab_works import LabWork
from app.database.models.subjects import Subject
from app.database.models.group_files import GroupFile
from app.database.models.teachers import Teacher
from app.database.models.groups import Group

class Assignment(Base):
    __tablename__ = 'assignments'
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    group_id: Mapped[int]=mapped_column(Integer, ForeignKey('groups.group_id', ondelete='CASCADE'), nullable=False)
    lab_id: Mapped[int] = mapped_column(Integer, ForeignKey('lab_works.id', ondelete='CASCADE'), nullable=False)
    teacher_id: Mapped[int] = mapped_column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'), nullable=False)
    created_at: Mapped[Date] = mapped_column(Date, nullable=False)
    deadline_at: Mapped[Date] = mapped_column(Date, nullable=False)
    status: Mapped[int] = mapped_column(Integer, nullable=False)
     # type: ignore
    teacher: Mapped["database.models.teachers.Teacher"] = relationship("database.models.teachers.Teacher", back_populates="assignment")
    lab_work: Mapped["database.models.lab_works.LabWork"] = relationship("database.models.lab_works.LabWork", back_populates="assignment")
    submission: Mapped["database.models.submissions.Submission"] = relationship("database.models.submissions.Submission",back_populates="assignment")
    group: Mapped["database.models.groups.Group"] = relationship("database.models.groups.Group",  back_populates="assignment")