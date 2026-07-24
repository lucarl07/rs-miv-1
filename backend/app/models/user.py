from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime
from datetime import datetime, timezone
from typing import List
from uuid import uuid4
from app.conn.db import Base


class User(Base):
    __tablename__ = "users"

    # ==== Colunas ====
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    nickname: Mapped[str] = mapped_column(String(30), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # ==== Relacionamentos ====
    key: Mapped["UserKey"] = relationship(
        back_populates="user", 
        uselist=False, cascade="all, delete-orphan"
    )
    messages: Mapped[List["Message"]] = relationship(
        back_populates="user"
    )
