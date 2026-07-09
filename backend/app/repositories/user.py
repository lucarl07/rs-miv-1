# Bibliotecas Nativas
import email
from typing import Literal

# Bibliotecas Externas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Módulos do Projeto
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.pw_hashing import hash_password 

# Funções Internas
async def _get_user_by_field(db: AsyncSession, field, value: str) -> User | None:
    result = await db.execute(select(User).where(field == value))
    return result.scalar_one_or_none()

# Funções Públicas
async def check_if_user_creds_exist(db: AsyncSession, nickname: str, email: str) -> bool:
    """Verifica se as credenciais fornecidas já estão sendo usadas
    por outro usuário."""

    existing = await db.execute(
        select(User).where(
            (User.nickname == nickname) | (User.email == email)
        )
    )

    if existing.scalar_one_or_none() is not None:
        return True

    return False

async def create_new_user(db: AsyncSession, data: UserCreate) -> User:
    new_user = User(
        nickname=data.nickname,
        email=data.email,
        hashed_password=hash_password(
            data.password.get_secret_value()
        ),
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user_by_id(db: AsyncSession, user_id: str) -> User:
    result = await db.execute(
        select(User)
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    return user

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    return await _get_user_by_field(db, User.email, email)

async def get_user_by_nickname(db: AsyncSession, nickname: str) -> User | None:
    return await _get_user_by_field(db, User.nickname, nickname)

