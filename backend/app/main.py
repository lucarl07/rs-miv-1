# Bibliotecas do Projeto
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Módulos do Projeto
from .conn import lifespan # Inclui DB + Redis
from .routers import router

app = FastAPI(lifespan=lifespan)
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

