from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, TIMESTAMP, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.psql import Base
import uuid
from datetime import datetime


class GroupSubject(Base):
    __tablename__ = 'group_subjects'
    group_id: Mapped[int] = mapped_column(Integer,  ForeignKey('groups.group_id', ondelete='CASCADE'), primary_key=True)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey('subjects.id', ondelete='CASCADE'), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    # Добавить отношения!!!
    group: Mapped["app.database.models.groups.Group"] = relationship("app.database.models.groups.Group",  back_populates="group_subject")  # type: ignore
    subject: Mapped["app.database.models.subjects.Subject"] = relationship("app.database.models.subjects.Subject",  back_populates="group_subject")  # type: ignore
