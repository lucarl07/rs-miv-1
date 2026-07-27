# Módulos do Projeto
from app.conn.db import get_db
from app.repositories.user import get_user_by_id
from app.schemas.message import ChatMessagePayload, IncomingMessage, MessageData
from app.utils.jwt import decode_access_token
from app.utils.ws import ws_manager
from app.repositories.message import save_message

# Bibliotecas Nativas
import json
import logging
from uuid import uuid4
from datetime import datetime, timezone

# Bibliotecas Externas
from fastapi import status
from fastapi import APIRouter
from fastapi import Depends
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ws", tags=["websockets"])

@router.websocket("") # Endpoint padrão
async def ws_chat(websocket: WebSocket, token: str, db: AsyncSession = Depends(get_db)):

    # Decodificando e validando o token:
    token_data = decode_access_token(token)
    if token_data is None or token_data.user_id is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    user = await get_user_by_id(db, token_data.user_id)
    if user is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
 
    nickname = user.nickname
    user_id = user.id

    # Tentando se conectar ao WebSocket:
    try:
        await ws_manager.connect(websocket, nickname, user_id, db)
    except Exception as e:
        logger.error(f"Erro ao estabelecer conexão para {nickname}: {e}")
        try:
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        except RuntimeError:
            pass
        return

    # Ao estar na conexão WebSocket:
    try:
        while True:
            data = json.loads(await websocket.receive_text()) 

            if data.get("type") == "heartbeat":
                await ws_manager.renew_presence(user_id)
                continue
            
            clean_msg = IncomingMessage(**data)
            stored_msg = await save_message(db, user_id, clean_msg.content)

            await ws_manager.broadcast(
                ChatMessagePayload(
                    type='message',
                    data=MessageData(
                        id=stored_msg.id,
                        nickname=nickname,
                        content=stored_msg.content,
                        timestamp=stored_msg.timestamp
                    )
                ).model_dump()
            )
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket, nickname, user_id)

        await ws_manager.broadcast({
            "type": "connection",
            "event": "leave",
            "nickname": nickname,
            "data": {
                "id": str(uuid4()),
                "nickname": "Mensagem do sistema",
                "content": f"{nickname} saiu do chat",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        })

