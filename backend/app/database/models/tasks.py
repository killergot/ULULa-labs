from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, TIMESTAMP, DateTime, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.psql import Base
import uuid
from datetime import datetime


class Task(Base):
    __tablename__ = 'tasks'

    task_id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True,
        autoincrement=True
    )
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        index=True
    )
    
    deadline: Mapped[Date] = mapped_column(Date, nullable=True)
    
    description: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    task_flag: Mapped[int] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,
                                                 nullable=True)

    user: Mapped["app.database.models.auth.User"] = relationship("app.database.models.auth.User", back_populates="tasks")
    links: Mapped[list["SharedLink"]] = relationship("SharedLink", back_populates="task",
                                                         cascade="all, delete-orphan")
