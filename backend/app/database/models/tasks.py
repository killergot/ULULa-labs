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
    
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        index=True
    )
    
    deadline: Mapped[Date] = mapped_column(Date, nullable=False)
    
    description: Mapped[str] = mapped_column(
        String(100), 
        nullable=False
    )

    # Опциональная связь с пользователем
    user: Mapped["app.database.models.auth.User"] = relationship("app.database.models.auth.User", back_populates="tasks")