from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_key import UserKey


async def upsert_public_key(db: AsyncSession, user_id: str, public_key: str) -> UserKey:
    result = await db.execute(
        select(UserKey).where(UserKey.user_id == user_id)
    )
    existing = result.scalar_one_or_none()

    if existing:
        existing.public_key = public_key
    else:
        existing = UserKey(user_id=user_id, public_key=public_key)
        db.add(existing)

    await db.commit()
    await db.refresh(existing)
    return existing


async def get_public_key(db: AsyncSession, user_id: str) -> UserKey | None:
    result = await db.execute(
        select(UserKey).where(UserKey.user_id == user_id)
    )
    return result.scalar_one_or_none()


