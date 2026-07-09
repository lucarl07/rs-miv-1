# Bibliotecas Nativas
from typing import Literal
from datetime import datetime

# Bibliotecas Externas
from pydantic import BaseModel, field_validator, field_serializer

# Módulos do Sistema
from app.utils.sanitization import msg_sanitizer


class IncomingMessage(BaseModel):
    """Schema de dados principais da mensagem de chat, exibidos na UI 
    do cliente."""

    content: str 

    @field_validator("content")
    @classmethod
    def sanitize_content(cls, v: str) -> str:
        sv = msg_sanitizer.clean(v)
        return sv


class MessageData(BaseModel):
    """Schema de dados principais da mensagem de chat, exibidos na UI 
    do cliente."""

    id: str
    nickname: str
    content: str 
    timestamp: datetime

    @field_serializer("timestamp")
    def serialize_timestamp(self, v: datetime) -> str:
        return v.isoformat()


class ChatMessagePayload(BaseModel):
    """Schema completo de uma mensagem de chat, incluindo seus dados 
    e metadados."""

    type: Literal["message"]
    data: MessageData


