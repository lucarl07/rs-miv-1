# Bibliotecas do Projeto
import json
from datetime import datetime, timezone
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, nickname: str):
        await websocket.accept()

        old = self.active_connections.get(nickname)
        if old is not None:
            await old.close()

        self.active_connections[nickname] = websocket

        await self.broadcast(json.dumps({
            "nickname": "%sys%",
            "content": f"{nickname} entrou no chat",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }))

    def disconnect(self, websocket: WebSocket, nickname: str):
        if self.active_connections.get(nickname) is websocket:
            del self.active_connections[nickname]

    async def broadcast(self, content: str):
        dead = []

        for nickname, connection in self.active_connections.items():
            try:
                await connection.send_text(content)
            except Exception:
                dead.append(nickname)

        for nickname in dead:
            del self.active_connections[nickname]

manager = ConnectionManager()

