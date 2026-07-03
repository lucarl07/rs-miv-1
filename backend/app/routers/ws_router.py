# Módulos do Projeto
from app.conn.db import get_db
from app.models.user import User
from app.utils.jwt import decode_access_token
from app.ws import repository
from app.utils.ws import ws_manager

# Bibliotecas Nativas
import json
from uuid import uuid4
from datetime import datetime, timezone

# Bibliotecas Externas
from fastapi import status
from fastapi import APIRouter
from fastapi import Depends
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/ws", tags=["websockets"])

@router.websocket("") # Endpoint padrão
async def ws_chat(websocket: WebSocket, token: str, db: AsyncSession = Depends(get_db)):

    # Decodificando e validando o token:
    token_data = decode_access_token(token)
    if token_data is None or token_data.user_id is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    result = await db.execute(select(User).where(User.id == token_data.user_id))
    user = result.scalar_one_or_none()
    if user is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
 
    nickname = user.nickname

    # Tentando se conectar ao WebSocket:
    await ws_manager.connect(websocket, nickname)

    try:
        while True:
            data = json.loads(await websocket.receive_text()) 
            content = data["content"]

            message = await repository.save_message(db, nickname, content)
            await ws_manager.broadcast(json.dumps({
                "id": message.id,
                "nickname": nickname,
                "content": content,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }))
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, nickname)

        await ws_manager.broadcast(json.dumps({
            "id": str(uuid4()),
            "nickname": "%sys%",
            "content": f"{nickname} saiu do chat",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }))

