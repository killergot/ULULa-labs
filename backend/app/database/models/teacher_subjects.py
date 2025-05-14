from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, TIMESTAMP, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.psql import Base
import uuid
from datetime import datetime


class TeacherSubject(Base):
    __tablename__ = 'teacher_subjects'
    teacher_id: Mapped[int] = mapped_column(Integer,  ForeignKey('teachers.id', ondelete='CASCADE'), primary_key=True)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey('subjects.id', ondelete='CASCADE'), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    # Добавить отношения!!!
    teachers: Mapped["app.database.models.teachers.Teacher"] = relationship("app.database.models.teachers.Teacher",  back_populates="teacher_subject")  # type: ignore
    subject: Mapped["app.database.models.subjects.Subject"] = relationship("app.database.models.subjects.Subject",  back_populates="teacher_subject")  # type: ignore
