from sqlalchemy.ext.asyncio import AsyncSession
from app.models.message import Message

async def save_message(db: AsyncSession, nickname: str, content: str) -> Message:
    message = Message(nickname=nickname, content=content) # Timestamp será gerada automaticamente no modelo Message
    db.add(message)
    await db.commit()
    return message;

