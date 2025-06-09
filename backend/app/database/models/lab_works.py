from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, TIMESTAMP, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.psql import Base
from datetime import datetime
from app.database.models.subjects import Subject
from app.database.models.group_files import GroupFile
from app.database.models.teachers import Teacher

class LabWork(Base):
    __tablename__ = 'lab_works'
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'), nullable=False)
    file_id: Mapped[int] = mapped_column(Integer, ForeignKey('group_files.id', ondelete='CASCADE'), nullable=True)


    subject: Mapped["database.models.subjects.Subject"] = relationship("database.models.subjects.Subject", back_populates="lab_work")  # type: ignore
    teacher: Mapped["database.models.teachers.Teacher"] = relationship("database.models.teachers.Teacher", back_populates="lab_work")
    files: Mapped["database.models.group_files.GroupFile"] = relationship("database.models.group_files.GroupFile", back_populates="lab_work")
    assignment: Mapped["database.models.assignments.Assignment"] = relationship("database.models.assignments.Assignment",
                                                                          back_populates="lab_work")

