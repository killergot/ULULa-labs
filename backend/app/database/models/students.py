from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, TIMESTAMP, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database.models.achievent import student_achievements
from app.database.models.subjects import student_subjects
from app.database.psql import Base
import uuid
from datetime import datetime


class Student(Base):
    __tablename__ = 'students'
    #from database.models.auth import User
    id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id', ondelete='CASCADE'),

        primary_key=True
    )
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey('groups.group_id', ondelete='CASCADE'), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    nickname: Mapped[str] = mapped_column(String(255), nullable=True)
    telegram: Mapped[str] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[str] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime,  default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    user: Mapped["database.models.auth.User"] = relationship("database.models.auth.User", back_populates="students")  # type: ignore
    group: Mapped["database.models.groups.Group"] = relationship("database.models.groups.Group", back_populates="students")

    achievements: Mapped[list["Achievement"]] = relationship(
        "Achievement",
        secondary=student_achievements,
        back_populates="students"
    )

    subjects: Mapped[list["Subject"]] = relationship(
        "Subject",
        secondary=student_subjects,
        back_populates="students"
    )