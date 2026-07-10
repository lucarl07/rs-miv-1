from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text
from app.conn.db import Base


class UserKey(Base):
    __tablename__ = 'user_keys'

    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    public_key: Mapped[str] = mapped_column(Text, nullable=True)

    # Por enquanto o relacionamento com User vai ser 1:1, mas em um futuro
    # próximo trocarei para 1:N (um User, uma ou mais UserKeys)
    user: Mapped["User"] = relationship(back_populates="key")

