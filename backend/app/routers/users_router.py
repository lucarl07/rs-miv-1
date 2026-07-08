# Bibliotecas Nativas
from typing import Annotated

# Bibliotecas Externas
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

# Módulos do Projeto
from app.conn.db import get_db
from app.models.user import User
from app.repositories.user import get_user_by_id
from app.schemas.user import UserOut
from app.utils.jwt import decode_access_token

router = APIRouter(prefix="/users", tags=["users"])
security = HTTPBearer()

@router.get("/me", response_model=UserOut)
async def get_current_user(
    auth: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: AsyncSession = Depends(get_db)
) -> User:
    access_token = auth.credentials
    token_data = decode_access_token(access_token)

    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credencial de acesso inválida e/ou expirada."
        )

    current_user = await get_user_by_id(db, token_data.user_id)
    return current_user
