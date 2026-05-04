# Módulos do Projeto
from app.db import get_db
from .manager import manager

# Bibliotecas Nativas
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
async def ws_chat(websocket: WebSocket, nickname: str):
    await manager.connect(websocket, nickname)
    try:
        while True:
            data = await websocket.receive_text()
            timestamp = datetime.now().strftime("%H:%M")
            await manager.broadcast(f"{nickname} ({timestamp} UTC-3):\n‖ {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, nickname)
        await manager.broadcast(f'  "{nickname}" saiu do chat.')


