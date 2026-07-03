# Bibliotecas Nativas
import os

# Bibliotecas do Projeto
from dotenv import load_dotenv
import redis.asyncio as redis

load_dotenv()
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

r = redis.from_url(REDIS_URL, decode_responses=True)
