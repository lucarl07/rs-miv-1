from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from app.models.message import Message
from app.schemas.message import ChatMessagePayload, MessageData

async def save_message(db: AsyncSession, user_id: str, content: str) -> Message:
    message = Message(content=content, user_id=user_id) 
    db.add(message)
    await db.commit()
    return message;

async def get_last_n_messages(db: AsyncSession, n: int = 100) -> list[dict]:
    stmt = (
        select(Message)
        .options(selectinload(Message.user))
        .order_by(Message.timestamp.desc())
        .limit(n)
    )
    result = await db.execute(stmt)
    messages = result.scalars().all()

    return [
        ChatMessagePayload(
            type="message",
            data=MessageData(
                id=msg.id,
                nickname=msg.user.nickname,
                content=msg.content,
                timestamp=msg.timestamp,
            ),
        ).model_dump(mode="json")
        for msg in reversed(messages)
    ]
