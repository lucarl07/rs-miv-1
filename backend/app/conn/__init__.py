# Bibliotecas Nativas
import base64
import secrets
import logging
from contextlib import asynccontextmanager

# Bibliotecas do Projeto
from fastapi import FastAPI

# Módulos do Projeto:
from .redis import r
from .db import Base, engine
import app.models # Importação necessária para sincronização não-lazy

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Função de ciclo de vida da aplicação."""

    # Redis inicializado e adicionado ao estado de aplicação:
    app.state.redis = r
    await app.state.redis.ping()

    # Conexão com o banco de dados efetuada:
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all) 

    # API fica online aqui:
    yield 

    # Fecha as conexões Redis de forma segura:
    await app.state.redis.aclose() 

