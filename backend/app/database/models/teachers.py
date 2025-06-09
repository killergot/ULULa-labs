
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, TIMESTAMP, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.psql import Base
import uuid
from datetime import datetime


class Teacher(Base):
    __tablename__ = 'teachers'
    #from database.models.auth import User
    id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    )
    FIO: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime,  default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    nickname: Mapped[str] = mapped_column(String(255), nullable=True)
    telegram: Mapped[str] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[str] = mapped_column(String(512), nullable=True)

    user: Mapped["database.models.auth.User"] = relationship("database.models.auth.User", back_populates="teachers")  # type: ignore
    teacher_subject: Mapped["database.models.teacher_subjects.TeacherSubject"] = relationship("database.models.teacher_subjects.TeacherSubject", back_populates="teachers",  cascade="all, delete-orphan")
    teacher_schedule: Mapped["database.models.teacher_schedule.TeacherSchedule"] = relationship(
        "database.models.teacher_schedule.TeacherSchedule", back_populates="teachers",  cascade="all, delete-orphan")
    lab_work: Mapped["app.database.models.lab_works.LabWork"] = relationship(
        "app.database.models.lab_works.LabWork", back_populates="teacher")

    assignment: Mapped["database.models.assignments.Assignment"] = relationship("database.models.assignments.Assignment",
                                                                          back_populates="teacher")
    #
