from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from app.database.psql import Base

# Вспомогательная таблица для связи многие-ко-многим
student_achievements = Table(
    'student_achievements',
    Base.metadata,
    Column('student_id', ForeignKey('students.id', ondelete='CASCADE'), primary_key=True),
    Column('achievement_id', ForeignKey('achievements.id', ondelete='CASCADE'), primary_key=True)
)

# Таблица ачивок
class Achievement(Base):
    __tablename__ = 'achievements'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    image_path: Mapped[str] = mapped_column(String(100), nullable=False, default = "frontiend\public\Achieve_1.jpg")

    students: Mapped[list["Student"]] = relationship(
        "Student",
        secondary=student_achievements,
        back_populates="achievements"
    )