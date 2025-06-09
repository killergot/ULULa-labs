from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.psql import Base
import uuid
from datetime import datetime


class Group(Base):
    __tablename__ = 'groups'
    group_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    group_number: Mapped[str] = mapped_column(String(50), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    students: Mapped["app.database.models.students.Student"] = relationship("app.database.models.students.Student",  back_populates="group")  # type: ignore
    schedule: Mapped["app.database.models.schedule.Schedule"] = relationship("app.database.models.schedule.Schedule",  back_populates="group")
    group_subject: Mapped["app.database.models.group_subjects.GroupSubject"] = relationship("app.database.models.group_subjects.GroupSubject",  back_populates="group")# type: ignore
    files: Mapped[list["app.database.models.group_files.GroupFile"]] = relationship(
        "app.database.models.group_files.GroupFile", back_populates="group", cascade="all, delete-orphan")
    assignment: Mapped["database.models.assignments.Assignment"] = relationship( "database.models.assignments.Assignment",back_populates="group")
