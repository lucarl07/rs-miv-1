# Bibliotecas Nativas
from typing import Literal
from datetime import datetime

# Bibliotecas Externas
from pydantic import BaseModel, Field, field_serializer


class IncomingMessage(BaseModel):
    """Schema de dados principais da mensagem de chat, com seu conteúdo 
    sendo criptografado e invisível ao servidor."""

    content: str = Field(
        max_length=6000, 
        description="""
            Conteúdo cifrado (IV + ciphertext) em base64 — o limite de 1000
            caracteres reais é validado no cliente antes da cifra; este 
            teto é só proteção contra payloads abusivos.
        """
    )


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


