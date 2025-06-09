from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, TIMESTAMP, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql.schema import Table

from app.database.psql import Base
import uuid
from datetime import datetime

student_subjects = Table(
    'student_subjects',
    Base.metadata,
    Column('student_id', ForeignKey('students.id', ondelete='CASCADE'), primary_key=True),
    Column('subject_id', ForeignKey('subjects.id', ondelete='CASCADE'), primary_key=True)
)


class Subject(Base):
    __tablename__ = 'subjects'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200),unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    # Добавить отношения!!!
    #students: Mapped["app.database.models.students.Student"] = relationship("app.database.models.students.Student",  back_populates="group")  # type: ignore
    #schedule: Mapped["app.database.models.schedule.Schedule"] = relationship("app.database.models.schedule.Schedule",  back_populates="group")  # type: ignore
    group_subject: Mapped["app.database.models.group_subjects.GroupSubject"] = relationship("app.database.models.group_subjects.GroupSubject", back_populates="subject")
    teacher_subject: Mapped["app.database.models.teacher_subjects.TeacherSubject"] = relationship("app.database.models.teacher_subjects.TeacherSubject", back_populates="subject")
    files: Mapped[list["app.database.models.group_files.GroupFile"]] = relationship(
        "app.database.models.group_files.GroupFile", back_populates="subject", cascade="all, delete-orphan")
    lab_work:  Mapped["app.database.models.lab_works.LabWorks"] = relationship(
        "app.database.models.lab_works.LabWork", back_populates="subject")
    students: Mapped[list["Student"]] = relationship(
        "Student",
        secondary=student_subjects,
        back_populates="subjects"
    )
