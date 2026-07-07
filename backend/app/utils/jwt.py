# Módulos do Projeto
from app.schemas.user import TokenData

# Bibliotecas Nativas
import os
from datetime import datetime, timedelta, timezone

# Bibliotecas Externas
from jose import JWTError, jwt

# Configuração 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 960 # 16 horas 

try:
    SECRET_KEY: str = os.environ["JWT_SECRET_KEY"]
except KeyError as exc:
    raise RuntimeError(
        "JWT_SECRET_KEY não definida. Configure essa variável no arquivo .env "
        "antes de iniciar a aplicação."
    ) from exc

# JWT 
def create_access_token(user_id: str, expires_delta: timedelta | None = None) -> str:
    """Gera um JWT cujo claim 'sub' é o UUID (id) do usuário.

    Usamos o id em vez do nickname porque o id é imutável, enquanto o
    nickname pode vir a ser alterado no futuro.

    Por padrão, o tempo de expiração para cada JWT é de 60 minutos após sua 
    criação.
    """
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = {"sub": user_id, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> TokenData | None:
    """Decodifica e valida um JWT, retornando o TokenData ou None se inválido/expirado."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")
        if user_id is None:
            return None
        return TokenData(user_id=user_id)
    except JWTError:
        return None
