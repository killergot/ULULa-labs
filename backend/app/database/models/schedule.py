
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, TIMESTAMP, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.psql import Base
import uuid
from datetime import datetime




    # Дни недели с JSON-данными
   




class Schedule(Base):
    __tablename__ = 'schedule'
    #from database.models.auth import User
    group_number: Mapped[str] = mapped_column(String(20),  ForeignKey('students.group_number', ondelete='CASCADE'), primary_key=True)
    week_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    monday: Mapped[dict] = mapped_column(JSON, nullable=True)
    tuesday: Mapped[dict] = mapped_column(JSON, nullable=True)
    wednesday: Mapped[dict] = mapped_column(JSON, nullable=True)
    thursday: Mapped[dict] = mapped_column(JSON, nullable=True)
    friday: Mapped[dict] = mapped_column(JSON, nullable=True)
    saturday: Mapped[dict] = mapped_column(JSON, nullable=True)
    sunday: Mapped[dict] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.utcnow)


    students: Mapped["database.models.students.Student"] = relationship("database.models.students.Student", back_populates="schedule")  # type: ignore
