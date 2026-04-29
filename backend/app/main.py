# Módulos do Projeto
from app.db import *

# Bibliotecas Locais
from datetime import datetime, timezone

# Bibliotecas do Projeto
from fastapi import FastAPI
from fastapi import Depends
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket, nickname: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        await self.broadcast(f'  "{nickname}" entrou no chat.')

    def disconnect(self, websocket: WebSocket, nickname: str):
        self.active_connections.remove(websocket)

    async def broadcast(self, content: str):
        for connection in self.active_connections:
            await connection.send_text(content)

manager = ConnectionManager()

@app.get("/")
async def root(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 'Hello World'"))
    value = result.scalar()
    return {"message": value}

@app.websocket("/ws") 
async def websocket_chat(websocket: WebSocket, nickname: str):
    await manager.connect(websocket, nickname)
    try:
        while True:
            data = await websocket.receive_text()
            timestamp = datetime.now().strftime("%H:%M")
            await manager.broadcast(f"{nickname} ({timestamp} UTC-3):\n‖ {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, nickname)
        await manager.broadcast(f'  "{nickname}" saiu do chat.')


