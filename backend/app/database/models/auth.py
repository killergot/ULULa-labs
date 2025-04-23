from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, TIMESTAMP, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.psql import Base
import uuid
from datetime import datetime
#from database.models.students import Student

# Модель пользователей (users)
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=True)  # Может быть NULL для OAuth
    role = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)  # Подтверждение email
    auth_provider: Mapped[str] = mapped_column(String(50), nullable=True)  # Провайдер OAuth
    provider_id: Mapped[str] = mapped_column(String(255), nullable=True)  # ID у провайдера OAuth
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.utcnow, nullable=True)

    # Определение отношений
    students: Mapped[list["database.models.students.Student"]] = relationship("database.models.students.Student", back_populates="user", cascade="all, delete-orphan")
    # tasks: Mapped[list["app.database.models.tasks.Task"]] = relationship("app.database.models.tasks.Task", back_populates="user", cascade="all, delete-orphan")
    sessions: Mapped[list["UserSession"]] = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    two_factor_codes: Mapped[list["TwoFactorCode"]] = relationship("TwoFactorCode", back_populates="user",
                                                                   cascade="all, delete-orphan")
    pending_2fa_sessions: Mapped[list["Pending2FASession"]] = relationship("Pending2FASession", back_populates="user",
                                                                           cascade="all, delete-orphan")


# Модель сессий пользователей (user_sessions)
class UserSession(Base):
    __tablename__ = 'user_sessions'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="sessions")


class TwoFactorCode(Base):
    __tablename__ = "two_factor_codes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    code = Column(String(6))
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="two_factor_codes")


class Pending2FASession(Base):
    __tablename__ = "pending_2fa_sessions"

    session_token = Column(String(36), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="pending_2fa_sessions")