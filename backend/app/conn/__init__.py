# Bibliotecas Nativas
import base64
import secrets
from contextlib import asynccontextmanager

# Bibliotecas do Projeto
from fastapi import FastAPI

# Módulos do Projeto:
from .redis import r
from .db import Base, engine
import app.models # Importação necessária para sincronização não-lazy

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Função de ciclo de vida da aplicação."""

    # Redis inicializado e adicionado ao estado de aplicação:
    app.state.redis = r
    await app.state.redis.ping()

    # Chave AES-256 para PGP gerada e adicionada ao Redis:
    session_key = secrets.token_bytes(32) # 256 bits
    b64_session_key = base64.b64encode(session_key).decode('ascii')
    await app.state.redis.set("session_key:global", b64_session_key)
    
    # Conexão com o banco de dados efetuada:
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all) 

    # API fica online aqui:
    yield 

    # Fecha as conexões Redis de forma segura:
    await app.state.redis.aclose() 

