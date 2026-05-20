# Módulos do Projeto
from app.db import get_db
from app.ws import repository
from app.ws.manager import manager

# Bibliotecas Nativas
import json
from datetime import datetime, timezone

# Bibliotecas Externas
from fastapi import APIRouter
from fastapi import Depends
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.get("/")
async def root(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 'Hello World'"))
    value = result.scalar()
    return {"message": value}

@router.websocket("/ws")
async def ws_chat(websocket: WebSocket, nickname: str, db: AsyncSession = Depends(get_db)):
    await manager.connect(websocket, nickname)

    try:
        while True:
            data = json.loads(await websocket.receive_text()) 
            content = data["content"]

            await repository.save_message(db, nickname, content)
            await manager.broadcast(json.dumps({
                "nickname": nickname,
                "content": content,
                "timestamp": datetime.now(timezone.utc).isoformat()
                # A RESOLVER: Não é estranho ter que usar 3 tempos 'diferentes'
                # sempre? Porque há o tempo do cliente, da API e do banco de 
                # dados...
            }))
    except WebSocketDisconnect:
        manager.disconnect(websocket, nickname)

        await manager.broadcast(json.dumps({
            "nickname": "%sys%",
            "content": f"{nickname} saiu do chat",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }))
