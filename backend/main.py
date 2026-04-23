from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from datetime import datetime, timezone

app = FastAPI()

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
def root():
    return {"message": "Hello World"}

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


