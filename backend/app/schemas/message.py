# Bibliotecas Nativas
from typing import Literal
from datetime import datetime

# Bibliotecas Externas
from pydantic import BaseModel, field_validator

# Módulos do Sistema
from app.utils.sanitization import msg_cleaner


class IncomingMessage(BaseModel):
    """Schema de dados principais da mensagem de chat, exibidos na UI 
    do cliente."""

    content: str 

    @field_validator("content")
    @classmethod
    def sanitize_content(cls, v: str) -> str:
        sv = msg_cleaner.clean(v)
        return sv


class MessageData(BaseModel):
    """Schema de dados principais da mensagem de chat, exibidos na UI 
    do cliente."""

    id: str
    nickname: str
    content: str
    timestamp: datetime

class ChatMessagePayload(BaseModel):
    """Schema completo de uma mensagem de chat, incluindo seus dados 
    e metadados."""

    type: Literal["message"]
    data: MessageData
