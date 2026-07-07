# Bibliotecas Nativas
from typing import Literal
from datetime import datetime

# Bibliotecas Externas
from pydantic import BaseModel

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
