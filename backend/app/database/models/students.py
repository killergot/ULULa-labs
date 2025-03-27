
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, TIMESTAMP, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.psql import Base
import uuid
from datetime import datetime


class Student(Base):
    __tablename__ = 'students'
    #from database.models.auth import User
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    )
    group_number: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.utcnow)


    user: Mapped["database.models.auth.User"] = relationship("database.models.auth.User", back_populates="students")  # type: ignore
    schedule: Mapped["database.models.schedule.Schedule"] = relationship("database.models.schedule.Schedule", back_populates="students")  