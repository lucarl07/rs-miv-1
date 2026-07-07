from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.message import Message
from app.schemas.message import ChatMessagePayload, MessageData

async def save_message(db: AsyncSession, nickname: str, content: str) -> Message:
    message = Message(nickname=nickname, content=content) # Timestamp será gerada automaticamente no modelo Message
    db.add(message)
    await db.commit()
    return message;

async def get_last_n_messages(db: AsyncSession, n: int = 100) -> list[dict]:
    result = await db.execute(
        select(Message)
        .order_by(Message.timestamp.desc())
        .limit(n)
    )
    messages = result.scalars().all()

    return [
        ChatMessagePayload(
            type="message",
            data=MessageData(
                id=msg.id,
                nickname=msg.nickname,
                content=msg.content,
                timestamp=msg.timestamp,
            ),
        ).model_dump(mode="json")
        for msg in reversed(messages)
    ]
