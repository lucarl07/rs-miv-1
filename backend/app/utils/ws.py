# Bibliotecas Nativas
import json
import logging
from uuid import uuid4
from datetime import datetime, timezone

# Bibliotecas Externas
from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

# Módulos do Projeto
from app.conn.redis import r
from app.repositories.message import get_last_n_messages
from app.repositories.user_key import get_public_key
from app.utils.pgp import encrypt_session_key
from app.utils.session_key import derive_session_key

logger = logging.getLogger(__name__)

PRESENCE_TTL = 30 # segundos
MISSING_PGP_KEY_CODE = 4001

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, nickname: str, user_id: str, db: AsyncSession):
        await websocket.accept()

        # Verificando por conexões duplicadas
        old = self.active_connections.get(nickname)
        if old is not None:
            await old.close()

        # Obtendo a chave pública (pubkey) do usuário e a chave de sessão (K) 
        public_key = await get_public_key(db, user_id)
        if public_key is None:
            await websocket.close(MISSING_PGP_KEY_CODE, "missing_pgp_key")
            return

        session_key = derive_session_key()

        # Encriptação de K com a pubkey + envio ao cliente
        encrypted_key = encrypt_session_key(public_key, session_key)
        await websocket.send_text(json.dumps({
            "type": "key_envelope",
            "encrypted_key": encrypted_key
        }))

        # Adicionando usuário conectado à lista de presença 
        self.active_connections[nickname] = websocket
        try:
            await r.set(f"presence:{user_id}", nickname, ex=PRESENCE_TTL)
        except Exception as e:
            logger.warning(f"""
                Failed to insert user into Redis presence list: {e}
            """)

        # Enviando a lista de presença em formato JSON
        try:
            keys = [key async for key in r.scan_iter(match="presence:*")]
            online_nicknames = await r.mget(keys) if keys else []
            await websocket.send_text(json.dumps({
                "type": "online_users",
                "users": online_nicknames
            }))
        except Exception as e:
            logger.warning(f"Failed to send list of online users: {e}")

        # Tenta buscar histórico de mensagens no Redis...
        try:
            cached = await r.lrange("chat:global:messages", 0, -1)
        except Exception as e:
            logger.warning(f"Failed to read Redis message cache: {e}")
            cached = []

        # ...se não, tenta obtê-lo do banco de dados.
        if cached:
            messages = [json.loads(m) for m in reversed(cached)]
        else:
            messages = await get_last_n_messages(db, n=100)

        # Envia o histórico de mensagens ao cliente
        await websocket.send_text(json.dumps({
            "type": "message_history",
            "messages": messages
        }))

        # Anuncia uma nova conexão para todos as conexões ativas.
        await self.broadcast({
            "type": "connection",
            "event": "join",
            "nickname": nickname,
            "data": {
                "id": str(uuid4()),
                "nickname": "Mensagem do sistema",
                "content": f"{nickname} entrou no chat",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        })

    async def disconnect(self, websocket: WebSocket, nickname: str, user_id: str):
        if self.active_connections.get(nickname) is websocket:
            del self.active_connections[nickname]

        try:
            await r.delete(f"presence:{user_id}")
        except Exception as e:
            logger.warning(f"""
                User not instantly removed from Redis presence list: {e}
            """)

    async def renew_presence(self, user_id: str):
        try:
            await r.expire(f"presence:{user_id}", PRESENCE_TTL)
        except Exception as e:
            logger.warning(f"""
               [SEVERE] User presence was not renewed on Redis: {e}
            """)

    async def broadcast(self, message_payload: dict):
        dead = []
        str_message_payload = json.dumps(message_payload)

        for nickname, connection in self.active_connections.items():
            try:
                await connection.send_text(str_message_payload)
            except Exception:
                dead.append(nickname)

        for nickname in dead:
            del self.active_connections[nickname]

        # Não vou mudar o tipo de message_payload por causa dessa bomba aqui:
        if message_payload.get("type") == "message": 
            try:
                await r.lpush("chat:global:messages", str_message_payload)
                await r.ltrim("chat:global:messages", 0, 99)
            except Exception as e:
                logger.warning(f"Failed to update Redis cache: {e}")

ws_manager = ConnectionManager()

