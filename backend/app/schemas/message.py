# Bibliotecas Nativas
from typing import Literal
from datetime import datetime

# Bibliotecas Externas
from pydantic import BaseModel, field_serializer


class IncomingMessage(BaseModel):
    """Schema de dados principais da mensagem de chat, com seu conteúdo 
    sendo criptografado e invisível ao servidor."""

    content: str 


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

