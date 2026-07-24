# Bibliotecas Nativas do Python
import os

# Bibliotecas do Projeto
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Módulos do Projeto
from .conn import lifespan # Inclui DB + Redis
from .routers import router

app = FastAPI(lifespan=lifespan)
app.include_router(router)

allowed_origins = [
    origin.strip() 
    for origin in os.environ["CORS_ALLOWED_ORIGINS"].split(",")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

