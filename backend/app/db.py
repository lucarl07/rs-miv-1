# Bibliotecas Locais
import os 

# Bibliotecas do Projeto
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

# Carregando variáveis de ambiente
load_dotenv()
DB_URL = os.getenv("DB_URL")

# Objetos para a conexão com o banco de dados
engine = create_async_engine(
    DB_URL, 
    connect_args={"check_same_thread": False}, 
    echo=True # Por enquanto, apenas para debugar
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()
    
# Função para efetuar conexão
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

