
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, TIMESTAMP, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.psql import Base
import uuid
from datetime import datetime


    # Дни недели с JSON-данными

class TeacherSchedule(Base):
    __tablename__ = 'teacher_schedule'
    __table_args__ = {"extend_existing": True}
    #from database.models.auth import User
    teacher_id: Mapped[int] = mapped_column(Integer,  ForeignKey('teachers.id', ondelete='CASCADE'), primary_key=True)
    week_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    monday: Mapped[dict] = mapped_column(JSON, nullable=True)
    tuesday: Mapped[dict] = mapped_column(JSON, nullable=True)
    wednesday: Mapped[dict] = mapped_column(JSON, nullable=True)
    thursday: Mapped[dict] = mapped_column(JSON, nullable=True)
    friday: Mapped[dict] = mapped_column(JSON, nullable=True)
    saturday: Mapped[dict] = mapped_column(JSON, nullable=True)
    sunday: Mapped[dict] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    teachers: Mapped["database.models.teachers.Teacher"] = relationship("database.models.teachers.Teacher",
                                                                 back_populates="teacher_schedule")

