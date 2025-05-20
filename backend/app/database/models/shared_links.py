from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, DateTime,UUID

from app.database.psql import Base
from datetime import datetime, timedelta
import uuid

def default_expiration():
    return datetime.utcnow() + timedelta(days=5)

class SharedLink(Base):
    __tablename__ = 'shared_links'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey('tasks.task_id'), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, default=default_expiration)

    task: Mapped["app.database.models.tasks.Task"] = relationship("app.database.models.tasks.Task", back_populates="links")