from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, DateTime
from datetime import datetime, timezone
from uuid import uuid4
from app.conn.db import Base

class Message(Base):
    __tablename__ = "messages"

    # ==== Colunas ====
    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("users.id")
    )
    content: Mapped[str] = mapped_column(
        String(2000), 
        nullable=False
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # ==== Relacionamentos ====
    user: Mapped["User"] = relationship(back_populates="messages")
