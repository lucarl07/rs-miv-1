from uuid import uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Text
from app.conn.db import Base


class UserKey(Base):
    __tablename__ = 'user_keys'

    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("users.id"), 
        unique=True, nullable=False
    )
    public_key: Mapped[str] = mapped_column(
        Text, 
        nullable=False
    )

    # Por enquanto o relacionamento com User vai ser 1:1, mas em um futuro
    # próximo trocarei para 1:N (um User, uma ou mais UserKeys)
    user: Mapped["User"] = relationship(back_populates="key")

