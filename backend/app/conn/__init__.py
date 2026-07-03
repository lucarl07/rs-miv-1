# Bibliotecas Nativas
from contextlib import asynccontextmanager

# Bibliotecas do Projeto
from fastapi import FastAPI

# Módulos do Projeto:
from .redis import r
from .db import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = r # 1. Inicializa o Redis
    
    async with engine.begin() as conn: # 2. Sincroniza tabelas do banco de dados
        await conn.run_sync(Base.metadata.create_all) 

    yield # 3. API fica online aqui
    
    await app.state.redis.aclose() # 4. Fecha as conexões Redis de forma segura

