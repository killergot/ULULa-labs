from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, TIMESTAMP, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.psql import Base
import uuid
from datetime import datetime

# Модель пользователей (users)
class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=True)  # Может быть NULL для OAuth
    role: Mapped[str] = mapped_column(String(50), default='user', nullable=False)  # Роль пользователя
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)  # Подтверждение email
    auth_provider: Mapped[str] = mapped_column(String(50), nullable=True)  # Провайдер OAuth
    provider_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)  # ID у провайдера OAuth
    is_2fa_enabled: Mapped[bool] = mapped_column(Boolean, default=False)  # Флаг двухфакторной аутентификации
    two_factor_secret: Mapped[str] = mapped_column(Text, nullable=True)  # Секрет для TOTP (Google Authenticator)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.utcnow)

    # Определение отношений
    sessions: Mapped[list["UserSession"]] = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    password_resets: Mapped[list["PasswordReset"]] = relationship("PasswordReset", back_populates="user", cascade="all, delete-orphan")
    oauth_accounts: Mapped[list["OAuthAccount"]] = relationship("OAuthAccount", back_populates="user", cascade="all, delete-orphan")
    oauth_tokens: Mapped[list["OAuthToken"]] = relationship("OAuthToken", back_populates="user", cascade="all, delete-orphan")
    two_factor_codes: Mapped[list["TwoFactorCode"]] = relationship("TwoFactorCode", back_populates="user", cascade="all, delete-orphan")


# Модель сессий пользователей (user_sessions)
class UserSession(Base):
    __tablename__ = 'user_sessions'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="sessions")


# Модель для сброса пароля (password_resets)
class PasswordReset(Base):
    __tablename__ = 'password_resets'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="password_resets")


# Модель для OAuth-аккаунтов (oauth_accounts)
class OAuthAccount(Base):
    __tablename__ = 'oauth_accounts'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)  # Например, Google, GitHub
    provider_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)  # ID пользователя у провайдера
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="oauth_accounts")


# Модель для хранения OAuth токенов (oauth_tokens)
class OAuthToken(Base):
    __tablename__ = 'oauth_tokens'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    access_token: Mapped[str] = mapped_column(Text, nullable=False)
    refresh_token: Mapped[str] = mapped_column(Text, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)  # Время истечения access_token
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="oauth_tokens")


# Модель для двухфакторной аутентификации (например, временные коды)
class TwoFactorCode(Base):
    __tablename__ = 'two_factor_codes'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    code: Mapped[str] = mapped_column(String(6), nullable=False)  # Временный код для 2FA
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)  # Время, когда код истечет
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="two_factor_codes")