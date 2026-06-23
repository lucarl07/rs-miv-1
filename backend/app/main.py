# Bibliotecas do Projeto
from fastapi import FastAPI

# Módulos do Projeto
from .db import Base
from .db import engine
from .router import router

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

