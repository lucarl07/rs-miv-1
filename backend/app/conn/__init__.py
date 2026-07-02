# Bibliotecas Nativas
from contextlib import asynccontextmanager

# Bibliotecas do Projeto
from fastapi import FastAPI

# Módulos do Projeto:
from .redis import r
from .db import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Inicializa o Redis
    app.state.redis = r

    # 2. Sincroniza tabelas do banco de dados
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield # API fica online aqui

    # 3. Fecha as conexões Redis de forma segura
    await app.state.redis.aclose()

