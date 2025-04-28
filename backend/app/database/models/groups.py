from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, TIMESTAMP, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.psql import Base
import uuid
from datetime import datetime


class Group(Base):
    __tablename__ = 'groups'
    group_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    group_number: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    # Добавить отношения!!!
    students: Mapped["app.database.models.students.Student"] = relationship("app.database.models.students.Student",  back_populates="group")  # type: ignore
