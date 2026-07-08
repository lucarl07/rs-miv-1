# Bibliotecas Nativas
from datetime import datetime

# Bibliotecas Externas
from pydantic import BaseModel, EmailStr, ConfigDict, Field, SecretStr, field_validator

# Módulos do Sistema
from app.utils.data_validation import check_pw_validity

class UserCreate(BaseModel):
    """Schema de entrada para o registro de um novo usuário."""

    nickname: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: SecretStr = Field() # Toda validação ocorre no field validator

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: SecretStr) -> SecretStr:
        pw = v.get_secret_value()
        check_pw_validity(pw)
        return v


class UserOut(BaseModel):
    """Schema de saída pós-registro."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    nickname: str
    email: EmailStr
    created_at: datetime


class UserLogin(BaseModel):
    """Schema de entrada para o login."""

    email: EmailStr
    password: str


class UserPublic(UserOut):
    """Schema de saída pública."""

    # Nada a declarar, por ora.


class Token(BaseModel):
    """Schema de resposta do login bem-sucedido."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Payload decodificado do JWT, usado internamente para identificar o usuário autenticado."""

    user_id: str 


