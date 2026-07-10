# Bibliotecas Nativas
from contextlib import asynccontextmanager

# Bibliotecas do Projeto
from fastapi import FastAPI

# Módulos do Projeto:
from .redis import r
from .db import Base, engine
import app.models # Importação necessária para sincronização não-lazy

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = r
    await app.state.redis.ping()
    
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all) 

    # API fica online aqui:
    yield 

    # Fecha as conexões Redis de forma segura:
    await app.state.redis.aclose() 

