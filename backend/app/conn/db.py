# Bibliotecas Nativas
import os
import re
from typing import AsyncGenerator 

# Bibliotecas do Projeto
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

# Carregando variáveis de ambiente
load_dotenv()

DB_URL = os.environ["DB_URL"]
DB_ECHO = os.environ.get("DB_ECHO", '0').strip().lower() in ('1', 'true', 'yes')

# Valida quais opções serão necessárias para efetuar conexão
connect_args = {}

if "sslmode=require" in DB_URL:
    DB_URL = re.sub(r"[?&]sslmode=require", "", DB_URL)
    if "?" not in DB_URL and "&" in DB_URL:
        DB_URL = DB_URL.replace("&", "?", 1)
    connect_args = {"ssl": "require"}

# Objetos para a conexão com o banco de dados
engine = create_async_engine(
    DB_URL, 
    connect_args=connect_args, 
    echo=DB_ECHO
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()
    
# Função para efetuar conexão
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

