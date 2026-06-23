# Módulos do Projeto
from app.db import get_db
from app.ws import repository
from app.ws.manager import manager

# Bibliotecas Nativas
import json
from uuid import uuid4
from datetime import datetime, timezone

# Bibliotecas Externas
from fastapi import APIRouter
from fastapi import Depends
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/ws", tags=["websockets"])

@router.websocket("") # Endpoint padrão
async def ws_chat(websocket: WebSocket, nickname: str, db: AsyncSession = Depends(get_db)):
    await manager.connect(websocket, nickname)

    try:
        while True:
            data = json.loads(await websocket.receive_text()) 
            content = data["content"]

            message = await repository.save_message(db, nickname, content)
            await manager.broadcast(json.dumps({
                "id": message.id,
                "nickname": nickname,
                "content": content,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }))
    except WebSocketDisconnect:
        manager.disconnect(websocket, nickname)

        await manager.broadcast(json.dumps({
            "id": str(uuid4()),
            "nickname": "%sys%",
            "content": f"{nickname} saiu do chat",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }))
