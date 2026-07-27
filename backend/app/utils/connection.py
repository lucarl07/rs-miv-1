# Bibliotecas Nativas
import re


def handle_neondb_connection_url(raw_url: str, db_adapter: str = "asyncpg"):
    """Transforma uma URL de conexão com o banco de dados Neon Postgres.

    Retorna uma lista cujo primeiro elemento é a URL pós-processada, e o
    segundo são os argumentos em formato de dicionário p/o SQLAlchemy."""

    final_url = raw_url
    arguments = {}
    
    if "sslmode=require" in raw_url or "channel_binding=require" in raw_url:
        final_url = re.sub(r"[?&](sslmode|channel_binding)=require", "", raw_url)

        if "?" not in final_url and "&" in final_url:
            final_url = final_url.replace("&", "?", 1)

        arguments = { "ssl": "require" }

    if not f"+{db_adapter}" in final_url:
        final_url = final_url.replace("://", f"+{db_adapter}://")

    return [ final_url, arguments ] 


