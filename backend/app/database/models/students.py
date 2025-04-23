
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, TIMESTAMP, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
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
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.utcnow)


    user: Mapped["database.models.auth.User"] = relationship("database.models.auth.User", back_populates="students")  # type: ignore
    group: Mapped["database.models.groups.Group"] = relationship("database.models.groups.Group", back_populates="students")