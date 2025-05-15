from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.psql import Base
from datetime import datetime


class GroupFile(Base):
    __tablename__ = "group_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    filesize: Mapped[int] = mapped_column(Integer, nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"))
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("groups.group_id", ondelete="CASCADE"))
    group: Mapped["Group"] = relationship("Group", back_populates="files")  # связь назад к Group
    subject: Mapped["Subject"] = relationship("Subject", back_populates="files")  # связь назад к Group
