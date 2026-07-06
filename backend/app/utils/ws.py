# Bibliotecas Nativas
import json
from uuid import uuid4
from datetime import datetime, timezone

# Bibliotecas Externas
from fastapi import WebSocket

# Módulos do Projeto
from app.conn.redis import r

PRESENCE_TTL = 30 # segundos

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, nickname: str, user_id: str):
        await websocket.accept()

        old = self.active_connections.get(nickname)
        if old is not None:
            await old.close()

        self.active_connections[nickname] = websocket
        await r.set(f"presence:{user_id}", nickname, ex=PRESENCE_TTL)

        await self.broadcast(json.dumps({
            "id": str(uuid4()),
            "nickname": "%sys%",
            "content": f"{nickname} entrou no chat",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }))

    async def disconnect(self, websocket: WebSocket, nickname: str, user_id: str):
        if self.active_connections.get(nickname) is websocket:
            del self.active_connections[nickname]

        await r.delete(f"presence:{user_id}")

    async def renew_presence(self, user_id: str):
        await r.expire(f"presence:{user_id}", PRESENCE_TTL)

    async def broadcast(self, content: str):
        dead = []

        for nickname, connection in self.active_connections.items():
            try:
                await connection.send_text(content)
            except Exception:
                dead.append(nickname)

        for nickname in dead:
            del self.active_connections[nickname]

ws_manager = ConnectionManager()

