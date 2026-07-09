# Bibliotecas Nativas
from typing import Literal

# Bibliotecas Externas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Módulos do Projeto
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.pw_hashing import hash_password 

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

async def get_user_by_unique(
    db: AsyncSession, value: str, fieldname: Literal['nickname', 'email']
) -> User:
    """Retorna o usuário com base em um atributo único que não seja
    seu identificador - ou seja, aceita ou 'nickname' ou 'email'."""

    if fieldname.strip().lower() == 'nickname':
        field = User.nickname
    elif fieldname.strip().lower() == 'email':
        field = User.email
    else:
        raise ValueError(f'''
            Nome de campo único do usuário "{fieldname}" não existente.
        ''')

    result = await db.execute(
        select(User).where(field == value)
    )
    user = result.scalar_one_or_none()
    return user

