from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field

class UserCreate(BaseModel):
    """Schema de entrada para o registro de um novo usuário."""

    nickname: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    """Schema de entrada para o login."""

    email: EmailStr
    password: str


class UserOut(BaseModel):
    """Schema de saída pública."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    nickname: str
    email: EmailStr
    created_at: datetime


class Token(BaseModel):
    """Schema de resposta do login bem-sucedido."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Payload decodificado do JWT, usado internamente para identificar o usuário autenticado."""

    user_id: str | None = None
