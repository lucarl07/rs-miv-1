# Bibliotecas Externas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Módulos do Projeto
from app.models.user import User

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

async def get_user_by_id(db: AsyncSession, user_id: str) -> User:
    result = await db.execute(
        select(User)
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    return user

