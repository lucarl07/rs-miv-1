# Bibliotecas do Projeto
import json
from datetime import datetime, timezone
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket, nickname: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        await self.broadcast(json.dumps({
            "nickname": "%sys%",
            "content": f"{nickname} entrou no chat",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }))

    def disconnect(self, websocket: WebSocket, nickname: str):
        self.active_connections.remove(websocket)

    async def broadcast(self, content: str):
        for connection in self.active_connections:
            await connection.send_text(content)

manager = ConnectionManager()

