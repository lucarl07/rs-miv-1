# Bibliotecas do Projeto
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Módulos do Projeto
from .db import Base
from .db import engine
from .router import router

app = FastAPI()
app.include_router(router)

origins = [
    "http://localhost:5173", # Front-end local
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

