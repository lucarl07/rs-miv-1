# Bibliotecas Externas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Módulos do Projeto
from app.models.user import User

async def get_user_by_id(db: AsyncSession, user_id: str) -> User:
    result = await db.execute(
        select(User)
        .where(User.id == user_id)
    )
    user = result.scalar_one()
    return user
