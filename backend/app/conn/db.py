# Bibliotecas Nativas
import os
from typing import AsyncGenerator 

# Bibliotecas do Projeto
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

# Módulos do Projeto
from app.utils.connection import handle_neondb_connection_url

# Carregando variáveis de ambiente
load_dotenv()

RAW_DB_URL = os.environ["DB_URL"]
DB_ECHO = os.environ.get("DB_ECHO", '0').strip().lower() in ('1', 'true', 'yes')

# Valida quais opções serão necessárias para efetuar conexão
database_url, connect_args = handle_neondb_connection_url(RAW_DB_URL)

# Objetos para a conexão com o banco de dados
engine = create_async_engine(
    database_url, 
    connect_args=connect_args, 
    echo=DB_ECHO
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()
    
# Função para efetuar conexão
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

